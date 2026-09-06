import os
import fitz  # pymupdf
from rag.embeddings import embed_text
from rag.db import insert_chunk

def chunk_text(text: str, chunk_size: int = 500, overlap: int = 50):
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk = " ".join(words[i:i + chunk_size])
        chunks.append(chunk)
        i += chunk_size - overlap
    return chunks

def extract_text_from_pdf(path: str) -> str:
    doc = fitz.open(path)
    text = "\n".join(page.get_text() for page in doc)
    doc.close()
    return text

def ingest_file(path: str):
    ext = os.path.splitext(path)[1].lower()
    if ext == ".pdf":
        text = extract_text_from_pdf(path)
    elif ext in (".txt", ".md"):
        with open(path, "r", encoding="utf-8", errors="ignore") as f:
            text = f.read()
    else:
        raise ValueError(f"Unsupported KB file type: {ext}")

    chunks = chunk_text(text)
    for idx, chunk in enumerate(chunks):
        embedding = embed_text(chunk)
        insert_chunk(path, idx, chunk, embedding)
    return len(chunks)

def ingest_directory(directory: str):
    results = {}
    for root, _, files in os.walk(directory):
        for fname in files:
            fpath = os.path.join(root, fname)
            try:
                n = ingest_file(fpath)
                results[fpath] = n
            except Exception as e:
                results[fpath] = f"error: {e}"
    return results