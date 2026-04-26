from sentence_transformers import SentenceTransformer
from pathlib import Path
import os
import torch

BASE_DIR  = Path(__file__).resolve().parent.parent
MODEL_DIR = BASE_DIR / "models" / "paraphrase-multilingual-mpnet-base-v2"

def get_embedding_model() -> SentenceTransformer:
    os.environ["TRANSFORMERS_OFFLINE"] = "1"
    os.environ["HF_DATASETS_OFFLINE"]  = "1"

    device = "cuda" if torch.cuda.is_available() else "cpu"

    if not MODEL_DIR.exists():
        raise FileNotFoundError(
            f"❌ Model tidak ditemukan di {MODEL_DIR}\n"
            f"   Jalankan dulu: python utils.py (perlu internet sekali)"
        )

    print(f"[Embeddings] ✅ Load dari lokal: {MODEL_DIR} | device: {device}")
    return SentenceTransformer(str(MODEL_DIR), device=device)