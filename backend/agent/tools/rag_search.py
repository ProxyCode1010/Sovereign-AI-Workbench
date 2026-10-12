from rag.embeddings import embed_text
from rag.db import search_similar

try:
    from langsmith import traceable
except ImportError:
    def traceable(*args, **kwargs):
        def decorator(func):
            return func
        return decorator

@traceable(name="rag_search", run_type="tool")
def rag_search(query: str, top_k: int = 5) -> list[dict]:
    emb = embed_text(query)
    return search_similar(emb, top_k)