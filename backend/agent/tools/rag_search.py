from rag.embeddings import embed_text
from rag.db import search_similar

def rag_search(query: str, top_k: int = 5) -> list[dict]:
    emb = embed_text(query)
    return search_similar(emb, top_k)