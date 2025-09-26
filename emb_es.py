from langchain_community.document_loaders import PyPDFLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain.schema import Document
import glob
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import ElasticsearchStore
from elasticsearch import Elasticsearch

DATA_PATH = "data"
ELASTIC_URL = "https://testnolimit-a75b01.es.us-central1.gcp.elastic.cloud:443"
INDEX_NAME = "kevynindex" 
ELASTIC_API_KEY = "VXhCZmdaa0J5SWdFN1FTaTBrMy06eE9xVUJraFhHVzFHbUFOS0V2LXRkZw=="

def main():
    generate_data_store()


def generate_data_store():
    documents = load_documents()
    chunks = split_text_semantic(documents)
    save_to_elasticsearch(chunks)


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
    text_splitter = RecursiveCharacterTextSplitter(
        chunk_size=300,
        chunk_overlap=50,
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


def save_to_elasticsearch(chunks):
    embeddings = HuggingFaceEmbeddings(model_name="google/embeddinggemma-300m")

    db = ElasticsearchStore.from_documents(
        documents=chunks,
        embedding=embeddings,
        index_name=INDEX_NAME,
        es_url=ELASTIC_URL,
        es_api_key=ELASTIC_API_KEY
    )

    print(f"Saved {len(chunks)} chunks to Elasticsearch index '{INDEX_NAME}'.")


if __name__ == "__main__":
    main()
