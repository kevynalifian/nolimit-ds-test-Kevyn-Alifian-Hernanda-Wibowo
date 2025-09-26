# nolimit-ds-test-Kevyn-Alifian-Hernanda-Wibowo
## 📖 Kemerdekaan Bot
### Introduction
Perkenalkan saya Kevyn Alifian Hernanda Wibowo izin memperkenalkan "📖 Kemerdekaan Bot" yang dibuat untuk memenuhi test data science dari NoLimit. 📖 Kemerdekaan Bot adalah Chatbot berbasis RAG tentang Sejarah Proklamasi Kemerdekaan Indonesia, yang dibangun menggunakan google/embeddinggemma-300m, meta-llama/Llama-3.1-8B-Instruct, dan Elasticsearch.

### Dasar pemilihan model
1. google/embeddinggemma-300m
- Ringan & Efisien → Model embedding berukuran kecil (300M parameter) sehingga cepat dipakai untuk menghasilkan representasi vektor teks.
- Kualitas Representasi Baik → Mampu menghasilkan embedding yang cukup bagus untuk semantic search, clustering, dan retrieval, meskipun ukurannya tidak besar.
- Hemat Resource → Bisa jalan di GPU menengah (misalnya T4 di Colab), tidak perlu hardware super besar.
- Kompatibel dengan pipeline retrieval → Cocok untuk dipakai bersama Elasticsearch, FAISS, atau vector store lainnya.

2. meta-llama/Llama-3.1-8B-Instruct
- Kemampuan Reasoning Lebih Tinggi → LLM ukuran 8B parameter yang cukup besar untuk reasoning, summarization, dan text generation dengan kualitas bagus.
- Optimasi untuk Instruction Following → Sudah di-fine-tune agar lebih baik dalam menjawab instruksi pengguna (seperti ChatGPT style).
- Lebih Ringan daripada Model Super Besar → Masih feasible dijalankan di GPU besar (A100 atau Colab Pro+), tidak seberat model 70B.
- Open-source & Fleksibel → Bisa dipakai offline dan dikustomisasi sesuai kebutuhan (fine-tuning, RAG, dsb).

3. Elasticsearch
- Mesin Pencari Skala Besar → Bisa menyimpan jutaan dokumen dengan query retrieval yang sangat cepat.
- Vector Search Support → Sekarang Elasticsearch sudah mendukung dense vector search → bisa dipakai untuk semantic search menggunakan embedding.
- Hybrid Search → Bisa menggabungkan keyword-based retrieval (BM25) dan semantic retrieval (dense embeddings) untuk hasil lebih relevan.
- Ekosistem Kuat → Banyak digunakan di industri, mudah diintegrasikan dengan aplikasi produksi.
- Scalability Tinggi → Bisa di-cluster untuk menangani data dalam jumlah besar.

### Dataset
Dataset yang digunakan berasal dari https://www.ksap.org/sap/wp-content/uploads/2020/07/MAJALAH-MAYA-KSAP-1-AGUSTUS-2020.pdf

### Set up Instructions:
1. Install library yang tersedia pada requirements.txt, dengan menjalankan kode pip install -r requirements.txt.
2. Jalankan tiap sel di file app_RAG.ipynb.
3. Jika pyngrok tidak berhasil menampilkan streamlit dari file app_RAG.ipynb.
4. Maka, saya sediakan file kemerdekaan_bot.py.
5. Untuk menjalankan file kemerdekaan_bot.py, cukup menggunakan kode streamlit run kemerdekaan_bot.py.
6. Aplikasi 📖 Kemerdekaan Bot siap digunakan.

### Cara penggunaan 📖 Kemerdekaan Bot:
1. Pengguna memasukkan pertanyaan pada kolom yang tersedia.
2. Klik button "Cari Jawaban", kemudian tunggu hingga jawaban ditampilkan.
3. Jika sudah, 📖 Kemerdekaan Bot akan menampilkan jawaban dari pertanyaannya, konteks chunk, dan asal konteks chunk dari halaman berapa pada data .pdf yang digunakan

### Flowchart
<img width="2826" height="2521" alt="Flowchart" src="https://github.com/user-attachments/assets/b0a86990-8f84-472e-83d7-f7491fc39b8e" />

