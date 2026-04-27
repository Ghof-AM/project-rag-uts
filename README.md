# 🤖 RAG Starter Pack — UTS Data Engineering

## Retrieval-Augmented Generation  
### Sistem Tanya-Jawab Cerdas Berbasis Dokumen

Dibuat dengan dikhususkan untuk mendapatkan informasi dari file berbentuk **CSV** atau **PDF** dengan lebih mudah tentang seputar laptop. Sistem ini dibangun berbasis **Starter Pack proyek RAG** untuk UTS Data Engineering D3/D4, kelompok masing-masing.

---

# 👥 Identitas Kelompok

| Nama | NIM | Tugas Utama |
|------|------|-------------|
| Adam Noverian | 244311033 | Data Engineering dan Demonstran sistem |
| Alfiyansyah W.P. | 244311034 | System Tester dan Project Manager |
| Ghofur Akbar M. | 244311042 | Pipeline Orchestrator |

- **Topik Domain:** Teknologi  
- **Stack yang Dipilih:** From Scratch  
- **LLM yang Digunakan:** Ollama  
- **Vector DB yang Digunakan:** FAISS  

---

# 🗂️ Struktur Proyek
# 🤖 RAG Starter Pack — UTS Data Engineering

## Retrieval-Augmented Generation  
### Sistem Tanya-Jawab Cerdas Berbasis Dokumen

Dibuat dengan dikhususkan untuk mendapatkan informasi dari file berbentuk **CSV** atau **PDF** dengan lebih mudah tentang seputar laptop. Sistem ini dibangun berbasis **Starter Pack proyek RAG** untuk UTS Data Engineering D3/D4, kelompok masing-masing.

---

# 👥 Identitas Kelompok

| Nama | NIM | Tugas Utama |
|------|------|-------------|
| Adam Noverian | 244311033 | Data Engineering dan Demonstran sistem |
| Alfiyansyah W.P. | 244311034 | System Tester dan Project Manager |
| Ghofur Akbar M. | 244311042 | Pipeline Orchestrator |

- **Topik Domain:** Teknologi  
- **Stack yang Dipilih:** From Scratch  
- **LLM yang Digunakan:** Ollama  
- **Vector DB yang Digunakan:** FAISS  

---

# 🗂️ Struktur Proyek

```bash
RAG-UTS-Kelompok 5/
├── data/
│   ├── acer_aspire_3.pdf
│   ├── deskripsi_laptop.csv
│   ├── harga_laptop.csv
│   ├── IdeaPad_Slim_3_14IAH8_Spec.pdf
│   ├── ThinkPad_T14_Gen_1_AMD_Spec.pdf
│   └── ThinkPad_T480_Spec.pdf
│
├── src/
│   ├── __init__.py
│   ├── embeddings.py        # 🔧 WAJIB DIISI: Pipeline indexing
│   ├── indexing.py          # 🔧 WAJIB DIISI: Pipeline query & retrieval
│   ├── query.py             # 🔧 WAJIB DIISI: Konfigurasi embedding
│   └── utils.py             # Downloader Model
│
├── ui/
│   └── app.py               # 🔧 WAJIB DIISI: Antarmuka Streamlit
│
├── docs/
│   ├── arsitektur.png       # 📌 Diagram arsitektur (buat sendiri)
│   └── Laporan UTS Data Engineering - kelompok 2.pdf
│
├── evaluation/
│   └── hasil_evaluasi.xlsx  # 📌 Tabel evaluasi 10 pertanyaan
│
├── .env.example             # Template environment variables
├── .gitignore
├── requirements.txt
└── README.md
```

# ⚡ Cara Memulai (Quickstart)
## 1. Clone & Setup
### Clone repository ini
```bash
git clone https://github.com/Ghof-AM/project-rag-uts.git
```
### Install dependencies
```bash
pip install -r requirements.txt
```
## 2. Siapkan Dokumen
#### Contoh: salin PDF atau TXT ke folder data
```bash
cp dokumen-saya.pdf data/
```
Letakkan dokumen sumber Anda di folder data/

## 3. Jalankan Indexing (sekali saja)
```bash
python -m src.indexing
```
## 4. Jalankan Sistem RAG
Dengan Streamlit UI
```bash
python -m streamlit run ui/app.py
```
# ⚙️ Parameter Default
| Parameter     | Default                               | Keterangan                    |
| ------------- | ------------------------------------- | ----------------------------- |
| CHUNK_SIZE    | 1000                                  |                               |
| CHUNK_OVERLAP | 200                                   |                               |
| TOP_K         | 8                                     |                               |
| MODEL_NAME    | paraphrase-multilingual-mpnet-base-v2 | Nama model LLM yang digunakan |


# 📊 Hasil Evaluasi
| NO                                  | Pertanyaan | Jawaban Sistem | Jawaban Ideal | Skor (1-5) |
| ---------------------------------- | ---------- | -------------- | ------------- | ---------- |
| 1 | Berapa harga Lenovo ThinkPad T14 Gen 1 Core i7 Touchscreen?           |     Harga Lenovo ThinkPad T14 Gen 1 Core i7 Touchscreen adalah Rp 3.850.000,0.           |        Harga: 3.850.000       |         5   |
| 2 | Jelaskan singkat deskripsi Lenovo ThinkPad T14 Gen 1 Core i7 Touchscreen         |     Lenovo ThinkPad T14 Gen 1 Core i7 Touchscreen adalah laptop modern dengan performa tinggi dan layar touchscreen. Cocok untuk kerja berat. Harganya Rp 3.850.000,0.      |        Laptop modern dengan performa tinggi dan layar touchscreen. Cocok untuk kerja berat.       |         5   |
| 3 | Apa laptop termurah di dataset, dan berapa harganya?           |    Laptop termurah di dataset adalah Lenovo G40-30 Celeron N2840 dengan harga Rp 1.190.000,0.           |        Acer Aspire One D270: 400.000    |         1  |
| 4 | Apa laptop termahal di dataset, dan berapa harganya?           |     Laptop termahal di dataset adalah HP EliteBook 845 G8 Ryzen 5 Pro 5650U dengan harga Rp 3.900.000.000            |        Advan Gaming Pixwar Ryzen 7 6800H Touchscreen: 9.199.000     |         1   |
| 5 | Sebutkan jumlah laptop dengan harga > 3.000.000          |     Jumlah laptop dengan harga > 3.000.000 adalah 14 unit.            |        43 item      |         1   |


# 🏗️ Arsitektur Sistem
```bash
RAG-UTS-Kelompok 5/docs/arsitektur.png
```
# 📚 Referensi & Sumber
- **Framework:** From Scratch
- **LLM:** Ollama
- **Vector DB:** FAISS docs
- **Tutorial yang digunakan:** AI guide

# 👨‍🏫 Informasi UTS
- **Mata Kuliah:** Data Engineering
- **Program Studi:** D4 Teknologi Rekayasa Perangkat Lunak
- **Deadline:** 26/04/2026

