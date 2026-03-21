from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent.parent
UPLOAD_DIR = BASE_DIR / "data" / "uploads"
CHROMA_DIR = BASE_DIR / "data" / "chroma_db"
LOCAL_MODEL_DIR = BASE_DIR / "local_models" / "all-MiniLM-L6-v2"

UPLOAD_DIR.mkdir(parents=True, exist_ok=True)
CHROMA_DIR.mkdir(parents=True, exist_ok=True)

EMBEDDING_MODEL = str(LOCAL_MODEL_DIR)
OLLAMA_MODEL = "llama3"