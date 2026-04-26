🤖 RAG Starter Pack — UTS Data Engineering
Retrieval-Augmented Generation — Sistem Tanya-Jawab Cerdas Berbasis Dokumen

Dibuat dengan dikhususkan untuk mendapatkan informasi dari file berbentuk csv atau pdf dengan lebih mudah tentang seputar laptop. sistem ini dibangun berbasis Starter pack proyek RAG untuk UTS Data Engineering D3/D4. kelompok masing-masing.

👥 Identitas Kelompok
Nama	              NIM        	Tugas Utama
Adam Noverian	    	244311033   Data Enginering dan Demonstran sistem
Alfiyansyah W.P.	  244311034   System Tester dan Project Manager
Ghofur Akbar M.	    244311042  	Pipeline Orchestrator
Topik Domain: (isi: Teknologi)
Stack yang Dipilih: (From Scratch)
LLM yang Digunakan: (Ollama)
Vector DB yang Digunakan: (FAISS)

🗂️ Struktur Proyek
RAG-UTS-Kelompok 5/
├── data/
│   ├── acer_aspire_3.pdf
│   ├── deskripsi_laptop.csv
│   ├── harga_laptop.csv
│   ├── IdeaPad_Slim_3_14IAH8_Spec.pdf
│   ├── ThinkPad_T14_Gen_1_AMD_Spec.pdf
│   └── ThinkPad_T480_Spec.pdf
├── src/
│   ├── __init__.py
│   ├── embeddings.py        # 🔧 WAJIB DIISI: Pipeline indexing
│   ├── indexing.py          # 🔧 WAJIB DIISI: Pipeline query & retrieval
│   ├── query.py             # 🔧 WAJIB DIISI: Konfigurasi embedding
│   └── utils.py             # Downloader Model
├── ui/
│   └── app.py               # 🔧 WAJIB DIISI: Antarmuka Streamlit
├── docs/
│   └── arsitektur.png       # 📌 Diagram arsitektur (buat sendiri)
│   └── Laporan UTS Data Engineering - kelompok 2.pdf
├── evaluation/
│   └── hasil_evaluasi.xlsx  # 📌 Tabel evaluasi 10 pertanyaan
├── .env.example             # Template environment variables
├── .gitignore
├── requirements.txt
└── README.md

⚡ Cara Memulai (Quickstart)
1. Clone & Setup
# Clone repository ini
git clone https://github.com/Ghof-AM/project-rag-uts.git

# Install dependencies
pip install -r requirements.txt

3. Siapkan Dokumen
Letakkan dokumen sumber Anda di folder data/:

# Contoh: salin PDF atau TXT ke folder data
cp dokumen-saya.pdf data/

4. Jalankan Indexing (sekali saja)
python -m src.indexing

6. Jalankan Sistem RAG
# Dengan Streamlit UI
 python -m streamlit run ui/app.py 

Parameter	Default	Keterangan
CHUNK_SIZE	1000	
CHUNK_OVERLAP	200	
TOP_K	8	
MODEL_NAME	(paraphrase-multilingual-mpnet-base-v2")	Nama model LLM yang digunakan
📊 Hasil Evaluasi
ada di dokumen Laporan UTS Data Engineering - kelompok 2.pdf
#	Pertanyaan	Jawaban Sistem	Jawaban Ideal	Skor (1-5)
ada di dokumen hasil_evaluasi.xlsx

🏗️ Arsitektur Sistem
ada di dokumen Arsitektur.png

📚 Referensi & Sumber
Framework: From Scratch
LLM: Ollama
Vector DB: FAISS docs
Tutorial yang digunakan: AI guide
👨‍🏫 Informasi UTS
Mata Kuliah: Data Engineering
Program Studi: D4 Teknologi Rekayasa Perangkat Lunak
Deadline: 26/04/2026
