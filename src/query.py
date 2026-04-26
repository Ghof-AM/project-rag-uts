import faiss
import pickle
import numpy as np
import ollama
from pathlib import Path
from rank_bm25 import BM25Okapi
from src.embeddings import get_embedding_model

BASE_DIR    = Path(__file__).resolve().parent.parent
INDEX_PATH  = BASE_DIR / "faiss_index.index"
CHUNKS_PATH = BASE_DIR / "chunks.pkl"


def load_index():
    if not INDEX_PATH.exists():
        raise FileNotFoundError("❌ Jalankan indexing.py dulu!")
    index = faiss.read_index(str(INDEX_PATH))
    with open(CHUNKS_PATH, "rb") as f:
        data = pickle.load(f)
    return index, data["chunks"], data["metadata"]


def retrieve_hybrid(query: str, embed_model, index, chunks, metadata, k=5):
    
    q_vec = np.array(
        embed_model.encode([query], normalize_embeddings=True),
        dtype=np.float32
    )


    scores_faiss, faiss_indices = index.search(q_vec, k * 2)
    max_score = scores_faiss[0].max() + 1e-9
    semantic_scores = {
        int(i): float(s / max_score)
        for i, s in zip(faiss_indices[0], scores_faiss[0])
        if i >= 0  
    }

    # BM25 Keyword Search
    tokenized   = [c.lower().split() for c in chunks]
    bm25        = BM25Okapi(tokenized)
    bm25_all    = bm25.get_scores(query.lower().split())
    max_bm25    = bm25_all.max() + 1e-9
    bm25_scores = {i: float(s / max_bm25) for i, s in enumerate(bm25_all)}

    # Hybrid: 65% semantic + 35% keyword
    alpha      = 0.65
    candidates = set(semantic_scores) | set(
        sorted(bm25_scores, key=bm25_scores.get, reverse=True)[:k * 2]
    )
    combined = {
        i: alpha * semantic_scores.get(i, 0) + (1 - alpha) * bm25_scores.get(i, 0)
        for i in candidates
    }
    top_ids = sorted(combined, key=combined.get, reverse=True)[:k]
    return [{"chunk": chunks[i], "metadata": metadata[i], "score": combined[i]}
            for i in top_ids]


def query_rag(query_text: str, k=5, chat_history=None, model_name="llama3.1:8b") -> dict:
    embed_model         = get_embedding_model()
    index, chunks, meta = load_index()
    results             = retrieve_hybrid(query_text, embed_model, index, chunks, meta, k)
    context_text        = "\n\n---\n\n".join([r["chunk"] for r in results])
    sources             = list({r["metadata"]["source"] for r in results})

    system_prompt = """Kamu adalah asisten pencarian dokumen yang cerdas dan teliti.
Tugasmu adalah menjawab pertanyaan pengguna HANYA berdasarkan konteks dokumen yang diberikan.

Aturan wajib:
1. Jawab dalam Bahasa Indonesia yang jelas dan terstruktur.
2. Jika pertanyaan meminta daftar/filter (contoh: "harga di atas X"), baca konteks dengan teliti dan filter hasilnya dengan benar.
3. Jika data tidak cukup untuk menjawab, katakan: "Informasi tidak tersedia dalam dokumen."
4. JANGAN mengarang data yang tidak ada di konteks.
5. Sertakan angka/detail spesifik dari konteks jika relevan."""

    user_prompt = f"""Dokumen referensi:
{context_text}

Pertanyaan pengguna: {query_text}

Berikan jawaban yang akurat dan langsung berdasarkan dokumen di atas."""

    messages = [{"role": "system", "content": system_prompt}]
    if chat_history:
        messages.extend(chat_history)
    messages.append({"role": "user", "content": user_prompt})

    response = ollama.chat(
        model=model_name,
        messages=messages,
        options={
            "temperature": 0.1,
            "top_p": 0.9,
            "num_ctx": 4096
        }
    )

    return {
        "answer":      response["message"]["content"],
        "sources":     sources,
        "chunks_used": [r["chunk"][:200] + "..." for r in results],
        "scores":      [round(r["score"], 3) for r in results],
    }