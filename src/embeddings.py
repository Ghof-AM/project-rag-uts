from sentence_transformers import SentenceTransformer
import torch

def get_embedding_model():
    """Load embedding model lokal — tidak butuh internet setelah download pertama."""
    device = "cuda" if torch.cuda.is_available() else "cpu"
    print(f"[Embeddings] Device: {device}")
   
    return SentenceTransformer("paraphrase-multilingual-mpnet-base-v2", device=device)