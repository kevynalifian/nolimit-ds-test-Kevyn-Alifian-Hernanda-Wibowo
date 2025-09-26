from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
from langchain_community.vectorstores import Chroma 
import os
import shutil
import glob
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

CHROMA_PATH = "chroma"
DATA_PATH = "data"

def main():
    generate_data_store()

def generate_data_store():
    documents = load_documents()
    chunks = split_text_semantic(documents)
    save_to_chroma(chunks)

def load_documents():
    documents = []
    pdf_files = glob.glob(f"{DATA_PATH}/*.pdf")
    for pdf in pdf_files:
        loader = PyPDFLoader(pdf)
        docs = loader.load()
        documents.extend(docs)
    print(f"Loaded {len(documents)} documents from {DATA_PATH}")
    return documents

def split_text_semantic(documents: list[Document]):
    """
    Memecah dokumen menjadi semantic chunks berdasarkan kalimat/paragraf
    dengan filtering untuk menghapus teks yang tidak relevan.
    """
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,         
        chunk_overlap=50,       
        length_function=len,
        separators=["\n\n", "\n", "."],  
        add_start_index=True
    )

    chunks = text_splitter.split_documents(documents)

    cleaned_chunks = []
    for chunk in chunks:
        text = chunk.page_content.replace("\n", " ").strip()

        chunk.page_content = text
        cleaned_chunks.append(chunk)

    print(f"Split {len(documents)} documents into {len(cleaned_chunks)} cleaned semantic chunks.")

    return cleaned_chunks


def save_to_chroma(chunks, reset_db=False):
    if reset_db and os.path.exists(CHROMA_PATH):
        shutil.rmtree(CHROMA_PATH)

    embeddings = HuggingFaceEmbeddings(model_name="google/embeddinggemma-300m")
    db = Chroma.from_documents(
        chunks,
        embeddings,
        persist_directory=CHROMA_PATH,
        collection_metadata={"hnsw:space": "l2"}
    )
    
    db.persist()
    del db
    print(f"Saved {len(chunks)} chunks to {CHROMA_PATH}.")

if __name__ == "__main__":
    main()