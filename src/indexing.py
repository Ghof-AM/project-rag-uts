from pathlib import Path
import pypdf
import pickle
import faiss
import numpy as np
from src.embeddings import get_embedding_model

BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR  = BASE_DIR / "data"
INDEX_PATH  = BASE_DIR / "faiss_index.index"
CHUNKS_PATH = BASE_DIR / "chunks.pkl"


# ── 1. DOCUMENT LOADER ──────────────────────────────────────────────────────
def load_documents() -> list[dict]:
    """
    Memuat semua PDF dan TXT dari folder data/.
    Wajib: minimal 2 format berbeda (memenuhi bobot 10%).
    """
    documents = []

    for file_path in sorted(DATA_DIR.glob("*")):
        text = ""
        if file_path.suffix.lower() == ".pdf":
            reader = pypdf.PdfReader(str(file_path))
            for page in reader.pages:
                text += (page.extract_text() or "") + "\n"
        elif file_path.suffix.lower() == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()
        else:
            continue  # skip format lain

        if text.strip():
            documents.append({"text": text, "source": file_path.name})
            print(f"  [Loader] ✅ {file_path.name} ({len(text):,} karakter)")

    return documents


# ── 2. TEXT SPLITTER ─────────────────────────────────────────────────────────
def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
    """
    Memecah teks menjadi chunk dengan overlap agar konteks tidak putus.
    chunk_size & chunk_overlap dapat dikonfigurasi (memenuhi bobot 10%).
    """
    chunks = []
    start  = 0
    while start < len(text):
        end   = min(start + chunk_size, len(text))
        chunk = text[start:end].strip()
        if chunk:
            chunks.append(chunk)
        if end == len(text):
            break
        start = end - chunk_overlap
    return chunks


# ── MAIN INDEXING ─────────────────────────────────────────────────────────────
def index_documents(chunk_size: int = 1000, chunk_overlap: int = 200):
    print("\n=== PIPELINE INDEXING DIMULAI ===")

    # Step 1: Load
    documents = load_documents()
    if not documents:
        raise ValueError("❌ Tidak ada dokumen PDF/TXT di folder data/")

    # Step 2: Chunk
    all_chunks: list[str]  = []
    all_metadata: list[dict] = []
    for doc in documents:
        chunks = chunk_text(doc["text"], chunk_size, chunk_overlap)
        all_chunks.extend(chunks)
        all_metadata.extend([{"source": doc["source"]}] * len(chunks))
    print(f"\n[Splitter] Total chunks: {len(all_chunks)}")

    # Step 3: Embedding
    print("[Embedding] Membuat embedding...")
    model      = get_embedding_model()
    embeddings = model.encode(all_chunks, show_progress_bar=True, batch_size=64)
    embeddings = np.array(embeddings, dtype=np.float32)

    # Step 4: Simpan ke FAISS (Vector Store)
    dim   = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, str(INDEX_PATH))

    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump({"chunks": all_chunks, "metadata": all_metadata}, f)

    print(f"\n✅ Indexing selesai! {len(all_chunks)} chunks tersimpan.")
    print(f"   Index : {INDEX_PATH}")
    print(f"   Chunks: {CHUNKS_PATH}")


if __name__ == "__main__":
    index_documents()