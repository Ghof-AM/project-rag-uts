from sentence_transformers import SentenceTransformer
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

MODELS = {
    
    "paraphrase-multilingual-mpnet-base-v2": "paraphrase-multilingual-mpnet-base-v2",
}

for folder_name, model_id in MODELS.items():
    save_path = BASE_DIR / "models" / folder_name
    print(f"Downloading '{model_id}' → {save_path}")
    model = SentenceTransformer(model_id)
    model.save(str(save_path))
    print(f"✅ Selesai: {folder_name}\n")
