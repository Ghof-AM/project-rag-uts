from pathlib import Path
import pypdf
import pickle
import faiss
import numpy as np
import pandas as pd
from src.embeddings import get_embedding_model

BASE_DIR    = Path(__file__).resolve().parent.parent
DATA_DIR    = BASE_DIR / "data"
INDEX_PATH  = BASE_DIR / "faiss_index.index"
CHUNKS_PATH = BASE_DIR / "chunks.pkl"


def load_documents() -> list[dict]:
    documents = []
    csv_data  = []

    for file_path in sorted(DATA_DIR.glob("*")):
        text = ""

        if file_path.suffix.lower() == ".pdf":
            reader = pypdf.PdfReader(str(file_path))
            for page in reader.pages:
                text += (page.extract_text() or "") + "\n"

        elif file_path.suffix.lower() == ".txt":
            with open(file_path, "r", encoding="utf-8") as f:
                text = f.read()

        elif file_path.suffix.lower() == ".csv":
            try:
                df = pd.read_csv(file_path)
                csv_data.append(df)
                print(f"  [Loader] ✅ CSV loaded: {file_path.name}")
            except Exception as e:
                print(f"  [Loader] ❌ Gagal baca CSV {file_path.name}: {e}")
        else:
            continue

        if text.strip():
            documents.append({"text": text, "source": file_path.name})
            print(f"  [Loader] ✅ {file_path.name} ({len(text):,} karakter)")

    if csv_data:
        try:
            merged_df = csv_data[0]
            for df in csv_data[1:]:
                merged_df = pd.merge(merged_df, df, on="name", how="outer")
            merged_df = merged_df.fillna("")

            text = "\n".join(
                f"nama: {row.get('name','')} | harga: {row.get('price','')} | deskripsi: {row.get('description','')}"
                for _, row in merged_df.iterrows()
            )
            documents.append({"text": text, "source": "merged_csv"})
            print(f"  [Loader] ✅ CSV digabung ({len(merged_df)} baris)")
        except Exception as e:
            print(f"  [Loader] ❌ Gagal merge CSV: {e}")

    return documents


def chunk_text(text: str, chunk_size: int = 1000, chunk_overlap: int = 200) -> list[str]:
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


def index_documents(chunk_size: int = 1000, chunk_overlap: int = 200):
    print("\n=== PIPELINE INDEXING DIMULAI ===")

    documents = load_documents()
    if not documents:
        raise ValueError("❌ Tidak ada dokumen di folder data/")

    all_chunks: list[str]    = []
    all_metadata: list[dict] = []
    for doc in documents:
        chunks = chunk_text(doc["text"], chunk_size, chunk_overlap)
        all_chunks.extend(chunks)
        all_metadata.extend([{"source": doc["source"]}] * len(chunks))
    print(f"\n[Splitter] Total chunks: {len(all_chunks)}")

    print("[Embedding] Membuat embedding...")
    model = get_embedding_model()

   
    embeddings = model.encode(
        all_chunks,
        show_progress_bar=True,
        batch_size=16,             
        normalize_embeddings=True   
    )
    embeddings = np.array(embeddings, dtype=np.float32)

    dim   = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  
    index.add(embeddings)
    faiss.write_index(index, str(INDEX_PATH))

    with open(CHUNKS_PATH, "wb") as f:
        pickle.dump({"chunks": all_chunks, "metadata": all_metadata}, f)

    print(f"\n✅ Indexing selesai! {len(all_chunks)} chunks tersimpan.")


if __name__ == "__main__":
    index_documents()