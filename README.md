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
│   └── acer_aspire_3.pdf 
│   └── deskripsi_laptop.csv
│   └── harga_laptop.csv
│   └── IdeaPad_Slim_3_14IAH8_Spec.pdf
│   └── ThinkPad_T14_Gen_1_AMD_Spec.pdf
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
├── evaluation/
│   └── hasil_evaluasi.xlsx  # 📌 Tabel evaluasi 10 pertanyaan
├── .env.example             # Template environment variables
├── .gitignore
├── requirements.txt
└── README.md

⚡ Cara Memulai (Quickstart)
1. Clone & Setup
# Clone repository ini
git clone https://github.com/[username]/rag-uts-[kelompok].git
cd rag-uts-[kelompok]

# Buat virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
# atau: venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
2. Konfigurasi API Key
# Salin template env
cp .env.example .env

# Edit .env dan isi API key Anda
# JANGAN commit file .env ke GitHub!
3. Siapkan Dokumen
Letakkan dokumen sumber Anda di folder data/:

# Contoh: salin PDF atau TXT ke folder data
cp dokumen-saya.pdf data/
4. Jalankan Indexing (sekali saja)
python src/indexing.py
5. Jalankan Sistem RAG
# Dengan Streamlit UI
streamlit run ui/app.py

# Atau via CLI
python src/query.py
🔧 Konfigurasi
Semua konfigurasi utama ada di src/config.py (atau langsung di setiap file):

Parameter	Default	Keterangan
CHUNK_SIZE	500	Ukuran setiap chunk teks (karakter)
CHUNK_OVERLAP	50	Overlap antar chunk
TOP_K	3	Jumlah dokumen relevan yang diambil
MODEL_NAME	(isi)	Nama model LLM yang digunakan
📊 Hasil Evaluasi
(Isi setelah pengujian selesai)

#	Pertanyaan	Jawaban Sistem	Jawaban Ideal	Skor (1-5)
1	...	...	...	...
2	...	...	...	...
Rata-rata Skor: ...
Analisis: ...

🏗️ Arsitektur Sistem
(Masukkan gambar diagram arsitektur di sini)

[Dokumen] → [Loader] → [Splitter] → [Embedding] → [Vector DB]
                                                         ↕
[User Query] → [Query Embed] → [Retriever] → [Prompt] → [LLM] → [Jawaban]
📚 Referensi & Sumber
Framework: (LangChain docs / LlamaIndex docs)
LLM: (Groq / Gemini / Ollama)
Vector DB: (ChromaDB / FAISS docs)
Tutorial yang digunakan: (cantumkan URL)
👨‍🏫 Informasi UTS
Mata Kuliah: Data Engineering
Program Studi: D4 Teknologi Rekayasa Perangkat Lunak
Deadline: (isi tanggal)
