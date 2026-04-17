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

# ── LOAD INDEX ──────────────────────────────────────────────────────────────
def load_index():
    if not INDEX_PATH.exists():
        raise FileNotFoundError("❌ faiss_index.index tidak ditemukan. Jalankan indexing.py dulu!")
    index = faiss.read_index(str(INDEX_PATH))
    with open(CHUNKS_PATH, "rb") as f:
        data = pickle.load(f)
    return index, data["chunks"], data["metadata"]


# ── RETRIEVER: HYBRID SEARCH (BONUS) ────────────────────────────────────────
def retrieve_hybrid(query: str, embed_model, index, chunks: list, metadata: list, k: int = 5):
    """
    Hybrid search: FAISS semantic + BM25 keyword.
    Menggabungkan dua skor untuk retrieval lebih akurat (fitur bonus).
    """
    # --- Semantic Search (FAISS) ---
    q_vec = np.array(embed_model.encode([query]), dtype=np.float32)
    distances, faiss_indices = index.search(q_vec, k * 2)

    # Normalisasi skor FAISS (semakin kecil distance = semakin relevan)
    max_dist = distances[0].max() + 1e-9
    semantic_scores = {int(i): 1 - (d / max_dist)
                       for i, d in zip(faiss_indices[0], distances[0])}

    # --- BM25 Keyword Search ---
    tokenized_corpus = [c.lower().split() for c in chunks]
    bm25             = BM25Okapi(tokenized_corpus)
    bm25_scores_all  = bm25.get_scores(query.lower().split())

    # Normalisasi BM25
    max_bm25 = bm25_scores_all.max() + 1e-9
    bm25_scores = {i: float(s / max_bm25)
                   for i, s in enumerate(bm25_scores_all)}

    # --- Gabungkan (alpha = bobot semantic) ---
    alpha = 0.6
    candidate_ids = set(semantic_scores.keys()) | set(
        sorted(bm25_scores, key=bm25_scores.get, reverse=True)[:k * 2]
    )
    combined = {
        i: alpha * semantic_scores.get(i, 0) + (1 - alpha) * bm25_scores.get(i, 0)
        for i in candidate_ids
    }
    top_ids = sorted(combined, key=combined.get, reverse=True)[:k]

    return [{"chunk": chunks[i], "metadata": metadata[i], "score": combined[i]}
            for i in top_ids]


# ── MAIN QUERY FUNCTION ──────────────────────────────────────────────────────
def query_rag(query_text: str, k: int = 5,
              chat_history: list = None, model_name: str = "llama3.1:8b") -> dict:
    """
    Pipeline query end-to-end dengan chat history (multi-turn, fitur bonus).
    """
    embed_model        = get_embedding_model()
    index, chunks, meta = load_index()

    # Step 1: Hybrid Retrieval
    results      = retrieve_hybrid(query_text, embed_model, index, chunks, meta, k)
    context_text = "\n\n---\n\n".join([r["chunk"] for r in results])

    # Step 2: Prompt Construction dengan source citation
    sources_list = list({r["metadata"]["source"] for r in results})
    sources_str  = ", ".join(sources_list)

    system_prompt = """Kamu adalah asisten dokumen yang membantu menjawab pertanyaan
berdasarkan konteks dokumen yang diberikan. Jawab secara lengkap, akurat, dan gunakan
Bahasa Indonesia. Jika informasi tidak ada di konteks, katakan dengan jelas."""

    user_prompt = f"""Konteks dari dokumen ({sources_str}):
{context_text}

Pertanyaan: {query_text}
Jawaban:"""

    # Step 3: Bangun messages (multi-turn chat history)
    messages = [{"role": "system", "content": system_prompt}]
    if chat_history:
        messages.extend(chat_history)
    messages.append({"role": "user", "content": user_prompt})

    # Step 4: Ollama LLM Generation
    response = ollama.chat(
        model=model_name,
        messages=messages,
        options={"temperature": 0.3, "top_p": 0.9}
    )

    answer = response["message"]["content"]

    return {
        "answer": answer,
        "sources": sources_list,
        "chunks_used": [r["chunk"][:200] + "..." for r in results],
        "scores": [round(r["score"], 3) for r in results],
    }


if __name__ == "__main__":
    print("=== CLI RAG — ketik 'exit' untuk keluar ===\n")
    history = []
    while True:
        q = input("Pertanyaan: ").strip()
        if q.lower() == "exit":
            break
        result = query_rag(q, chat_history=history)
        print("\n=== JAWABAN ===")
        print(result["answer"])
        print(f"\nSumber: {', '.join(result['sources'])}")
        print(f"Skor relevansi: {result['scores']}\n")

        # Simpan ke history untuk multi-turn
        history.append({"role": "user",      "content": q})
        history.append({"role": "assistant", "content": result["answer"]})