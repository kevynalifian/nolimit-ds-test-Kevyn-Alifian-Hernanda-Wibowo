import streamlit as st
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import ElasticsearchStore
from langchain_huggingface import HuggingFacePipeline
from transformers import pipeline

ELASTIC_URL = "https://testnolimit-a75b01.es.us-central1.gcp.elastic.cloud:443"
INDEX_NAME = "kevynindex" 
ELASTIC_API_KEY = "VXhCZmdaa0J5SWdFN1FTaTBrMy06eE9xVUJraFhHVzFHbUFOS0V2LXRkZw=="

# Prompt template
PROMPT_TEMPLATE = """
<start_of_turn>user
Jawablah pertanyaan di bawah ini hanya dengan mengutip dari konteks. 
Jika tidak ada jawaban di konteks, jawab: "Informasi tidak tersedia".

Konteks:
{context}

Pertanyaan:
{question}<end_of_turn>
<start_of_turn>model
"""

# Load embedding & DB
@st.cache_resource
def load_db():
    try:
        # Inisialisasi HuggingFaceEmbeddings
        embedding_function = HuggingFaceEmbeddings(
            model_name="google/embeddinggemma-300m"
        )
        
        # Buat koneksi ElasticsearchStore
        db = ElasticsearchStore(
            es_url=ELASTIC_URL,
            index_name=INDEX_NAME,
            es_api_key=ELASTIC_API_KEY,
            embedding=embedding_function
        )
        return db
    except Exception as e:
        st.error(f"Failed to connect to Elasticsearch: {e}")
        return None

def rag_answer(query_text: str):
    db = load_db()
    if db is None:
        return [], "Gagal memuat koneksi database.", []

    # Cari dokumen relevan menggunakan pencarian vektor
    results = db.similarity_search_with_relevance_scores(query_text, k=3)

    # Kalau tidak ada hasil relevan
    # Catatan: ElasticsearchStore dari Langchain_community tidak selalu mengembalikan skor relevansi, 
    # jadi kita bisa cek langsung apakah ada hasil.
    if not results:
        return [], "⚠️ Tidak ditemukan konteks yang relevan.", []

    # Gabungkan context
    context_text = "\n\n---\n\n".join([doc.page_content for doc, _ in results])

    # Buat prompt yang sudah diformat
    prompt = PROMPT_TEMPLATE.format(context=context_text, question=query_text)

    # 🔹 Load model open-source (Gemma 3B IT)
    generator = pipeline(
        task="text-generation",
        model="meta-llama/Llama-3.1-8B-Instruct",
        device=0,  # pakai GPU kalau ada, CPU = -1
        do_sample=True,
        temperature=0.2,
    )

    llm = HuggingFacePipeline(pipeline=generator)
    
    # Perbaikan Logika: Ambil respons dari LLM
    response = llm.invoke(prompt)
    
    # Logika untuk membuang prompt dari respons
    if isinstance(response, str):
        try:
            answer_start = response.index("<start_of_turn>model") + len("<start_of_turn>model")
            answer = response[answer_start:].strip()
        except ValueError:
            answer = response
    else:
        answer = str(response)

    # Ambil metadata source (nama file + halaman kalau ada)
    sources = []
    for doc, _ in results:
        # Langchain_community ElasticsearchStore menyimpan metadata di field 'metadata'
        src_meta = doc.metadata
        src = src_meta.get("source", "Unknown")
        page = src_meta.get("page", None)
        if page is not None:
            sources.append(f"{src} (halaman {page+1})")
        else:
            sources.append(src)

    # Return sesuai urutan: chunk, answer, source
    chunks = [doc.page_content for doc, _ in results]
    return chunks, answer.strip(), sources

# =========================
# Streamlit UI (Tidak ada perubahan)
# =========================
st.set_page_config(page_title="📖 RAG Demo", page_icon="📚")
st.title("📖 Kemerdekaan Bot")
st.write("Chatbot tentang Sejarah Proklamasi Kemerdekaan Indonesia.")
st.write("Chatbot berbasis RAG ini dibangun menggunakan google/embeddinggemma-300m, meta-llama/Llama-3.1-8B-Instruct, dan Elasticsearch.")

user_query = st.text_input("Masukkan pertanyaan Anda:")

if st.button("Cari Jawaban") and user_query:
    with st.spinner("Sedang mencari jawaban..."):
        chunks, answer, sources = rag_answer(user_query)

    st.subheader("Jawaban")
    st.write(answer)
    
    with st.expander("Lihat Context pada Chunk"):
        for i, chunk in enumerate(chunks, 1):
            st.markdown(f"**Chunk {i}:**\n\n{chunk}")
    st.subheader("Sumber Dokumen untuk Chunk")
    for i, src in enumerate(sources, 1):

        st.write(f"{i}. {src}")
