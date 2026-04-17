from sentence_transformers import SentenceTransformer
import torch

def get_embedding_model():
    """Load embedding model lokal — tidak butuh internet setelah download pertama."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[Embeddings] Device: {device}")
    # all-MiniLM-L6-v2: ringan (80MB), cepat, akurasi bagus untuk Bahasa Inggris
    # Alternatif multibahasa: "paraphrase-multilingual-MiniLM-L12-v2"
    return SentenceTransformer("all-MiniLM-L6-v2", device=device)