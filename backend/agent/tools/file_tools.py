import os
from config import UPLOAD_DIR, OUTPUT_DIR

try:
    from langsmith import traceable
except ImportError:
    def traceable(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

@traceable(name="read_file", run_type="tool")
def read_file(filename: str) -> str:
    path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(path):
        raise FileNotFoundError(filename)
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        return f.read()

@traceable(name="write_output_file", run_type="tool")
def write_output_file(filename: str, content: str) -> str:
    path = os.path.join(OUTPUT_DIR, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)
    return path

def list_uploads() -> list[str]:
    return os.listdir(UPLOAD_DIR)