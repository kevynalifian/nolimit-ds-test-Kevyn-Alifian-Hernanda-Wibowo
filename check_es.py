from elasticsearch import Elasticsearch

ELASTIC_URL = "https://testnolimit-a75b01.es.us-central1.gcp.elastic.cloud:443"
INDEX_NAME = "kevynindex" 
ELASTIC_API_KEY = "VXhCZmdaa0J5SWdFN1FTaTBrMy06eE9xVUJraFhHVzFHbUFOS0V2LXRkZw=="

client = Elasticsearch(
    ELASTIC_URL,
    api_key=ELASTIC_API_KEY,
    verify_certs=True
)
from elasticsearch import Elasticsearch

ELASTIC_URL = "https://testnolimit-a75b01.es.us-central1.gcp.elastic.cloud:443"
INDEX_NAME = "kevynindex" 
ELASTIC_API_KEY = "VXhCZmdaa0J5SWdFN1FTaTBrMy06eE9xVUJraFhHVzFHbUFOS0V2LXRkZw=="

# Connect ke Elasticsearch
client = Elasticsearch(
    ELASTIC_URL,
    api_key=ELASTIC_API_KEY,
    verify_certs=True
)

# Cek apakah index ada
if client.indices.exists(index=INDEX_NAME):
    print(f"✅ Index '{INDEX_NAME}' ditemukan.")

    # Ambil 5 dokumen pertama
    response = client.search(
        index=INDEX_NAME,
        body={
            "query": {"match_all": {}},
            "size": 5
        }
    )

    print("=== 5 Dokumen Pertama ===")
    for i, hit in enumerate(response["hits"]["hits"], start=1):
        source = hit["_source"]
        print(f"\n📄 Doc {i}:")
        print(source)
else:
    print(f"❌ Index '{INDEX_NAME}' tidak ditemukan.")

