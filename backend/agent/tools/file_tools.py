import os
from config import UPLOAD_DIR, OUTPUT_DIR

def read_file(filename: str) -> str:
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(filename)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

def write_output_file(filename: str, content: str) -> str:
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

def list_uploads() -> list[str]:
    return os.listdir(UPLOAD_DIR)