# RAG Starter Pack — UTS Data Engineering
## Retrieval-Augmented Generation — Sistem Tanya-Jawab Cerdas Berbasis Dokumen

> Dikhususkan untuk mendapatkan informasi dari file berbentuk **CSV** atau **PDF** seputar **laptop** dengan lebih mudah.  
> Sistem ini dibangun berbasis Starter Pack proyek RAG untuk **UTS Data Engineering**, per kelompok masing-masing.

---

## 👥 Identitas Kelompok

| Nama | NIM | Tugas Utama |
|------|-----|-------------|
| Adam Noverian | 244311033 | Data Engineering & Demonstran Sistem |
| Alfiyansyah W.P. | 244311034 | System Tester & Project Manager |
| Ghofur Akbar M. | 244311042 | Pipeline Orchestrator |

- **Topik Domain:** Teknologi (Laptop)
- **Stack yang Dipilih:** From Scratch
- **LLM yang Digunakan:** Ollama
- **Vector DB yang Digunakan:** FAISS

---

## 🗂️ Struktur Proyek

```
RAG-UTS-Kelompok-5/
├── data/                          # Dokumen sumber (PDF & CSV)
│   ├── acer_aspire_3.pdf
│   ├── deskripsi_laptop.csv
│   ├── harga_laptop.csv
│   ├── IdeaPad_Slim_3_14IAH8_Spec.pdf
│   ├── ThinkPad_T14_Gen_1_AMD_Spec.pdf
│   └── ThinkPad_T480_Spec.pdf
├── src/
│   ├── __init__.py
│   ├── embeddings.py              # Konfigurasi model embedding
│   ├── indexing.py                # Pipeline pemrosesan dokumen ke Vector DB
│   └── query.py                   # Logika retrieval dan augmentasi ke LLM
├── ui/
│   └── app.py                     # Interface Streamlit
├── docs/
│   ├── arsitektur.png             # Diagram arsitektur sistem
│   └── Laporan UTS Data Engineering - Kelompok 5.pdf
├── evaluation/
│   └── hasil_evaluasi.xlsx        # Tabel evaluasi 10 pertanyaan
├── .env.example                   # Template environment variables
├── .gitignore
├── requirements.txt               # Daftar library Python
└── README.md
```

---

## ⚡ Cara Memulai (Quickstart)

### 1. Clone & Setup

```bash
# Clone repository ini
git clone https://github.com/Ghof-AM/project-rag-uts.git
cd project-rag-uts

# Buat virtual environment
python -m venv venv
source venv/bin/activate        # Linux/Mac
# atau: venv\Scripts\activate   # Windows

# Install dependencies
pip install -r requirements.txt
```

### 2. Konfigurasi Environment

```bash
# Salin template env
cp .env.example .env

# Edit .env dan sesuaikan konfigurasi Anda
# JANGAN commit file .env ke GitHub!
```

### 3. Siapkan Dokumen

Letakkan dokumen sumber Anda di folder `data/`:

```bash
# Contoh: salin PDF atau CSV ke folder data
cp spesifikasi-laptop.pdf data/
cp harga-laptop.csv data/
```

### 4. Jalankan Indexing

```bash
python src/indexing.py
```

### 5. Jalankan Sistem RAG

```bash
# Dengan Streamlit UI
streamlit run ui/app.py
```

---

## 🔧 Konfigurasi

Semua konfigurasi utama dapat diatur langsung di setiap file `src/`:

| Parameter | Default | Keterangan |
|-----------|---------|------------|
| `CHUNK_SIZE` | 500 | Ukuran setiap chunk teks (karakter) |
| `CHUNK_OVERLAP` | 50 | Overlap antar chunk |
| `TOP_K` | 3 | Jumlah dokumen relevan yang diambil |
| `MODEL_NAME` | ollama (lokal) | Mesin AI untuk pemrosesan jawaban |
| `VECTOR_DB` | FAISS | Database vektor untuk penyimpanan embedding |

---

## 📊 Hasil Evaluasi

| # | Pertanyaan | Jawaban Sistem | Jawaban Ideal | Skor (1-5) |
|---|-----------|----------------|---------------|------------|
| 1 | ... | ... | ... | ... |
| 2 | ... | ... | ... | ... |
| 3 | ... | ... | ... | ... |
| 4 | ... | ... | ... | ... |
| 5 | ... | ... | ... | ... |
| 6 | ... | ... | ... | ... |
| 7 | ... | ... | ... | ... |
| 8 | ... | ... | ... | ... |
| 9 | ... | ... | ... | ... |
| 10 | ... | ... | ... | ... |

**Rata-rata Skor:** ...  
**Analisis:** ...

---

## 🏗️ Arsitektur Sistem

> *(Masukkan gambar diagram arsitektur di sini — lihat `docs/arsitektur.png`)*

```
[Dokumen PDF/CSV]
       |
       ▼
   [Loader]          ← src/indexing.py
       |
       ▼
  [Text Splitter]    ← Chunking dengan CHUNK_SIZE & CHUNK_OVERLAP
       |
       ▼
  [Embedding Model]  ← src/embeddings.py (Ollama)
       |
       ▼
  [Vector DB FAISS]  ← Penyimpanan vektor lokal
       |
       ▼ (saat query)
  [Retriever]        ← src/query.py — ambil TOP_K dokumen relevan
       |
       ▼
  [Prompt Builder]   ← Gabungkan konteks + pertanyaan user
       |
       ▼
  [LLM Ollama]       ← Generate jawaban
       |
       ▼
  [Jawaban User]     ← Tampil di UI Streamlit (ui/app.py)
```

---

## 📚 Data yang Digunakan

Sistem ini menggunakan dokumen spesifikasi dan harga laptop berikut:

| File | Tipe | Deskripsi |
|------|------|-----------|
| `acer_aspire_3.pdf` | PDF | Spesifikasi Acer Aspire 3 |
| `IdeaPad_Slim_3_14IAH8_Spec.pdf` | PDF | Spesifikasi Lenovo IdeaPad Slim 3 |
| `ThinkPad_T14_Gen_1_AMD_Spec.pdf` | PDF | Spesifikasi ThinkPad T14 Gen 1 AMD |
| `ThinkPad_T480_Spec.pdf` | PDF | Spesifikasi ThinkPad T480 |
| `deskripsi_laptop.csv` | CSV | Deskripsi umum berbagai laptop |
| `harga_laptop.csv` | CSV | Data harga laptop |

---

## 🛠️ Teknologi yang Digunakan

- **[Ollama](https://ollama.com/)** — LLM lokal untuk inferensi
- **[FAISS](https://github.com/facebookresearch/faiss)** — Vector database lokal dari Meta
- **[Streamlit](https://streamlit.io/)** — Framework UI berbasis Python
- **[LangChain](https://www.langchain.com/)** *(opsional)* — Orkestrasi pipeline RAG

---

## 👨‍💻 Kontribusi

Proyek ini dibuat untuk keperluan **UTS Data Engineering** — Kelompok 5.  
Silakan fork dan kembangkan sesuai kebutuhan.

---

*© 2026 Kelompok 5 — Data Engineering *
