import os

BASE_DIR = os.getcwd()
UPLOAD_DIR = os.path.join(BASE_DIR, "data")
os.makedirs(UPLOAD_DIR, exist_ok=True)

CHROMA_DB_PATH = os.path.join(BASE_DIR, "chroma_db")

# Qwen 4B API
QWEN_API_URL = "http://127.0.0.1:1234/v1/responses"  # replace with your LM Studio endpoint
QWEN_MODEL = "qwen/qwen3-vl-4b"
TOP_K = 5
