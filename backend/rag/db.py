import psycopg2
from config import DATABASE_URL

def get_conn():
    return psycopg2.connect(DATABASE_URL)

def insert_chunk(source_path: str, chunk_index: int, content: str, embedding: list[float]):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO documents (source_path, chunk_index, content, embedding) VALUES (%s, %s, %s, %s)",
        (source_path, chunk_index, content, embedding),
    )
    conn.commit()
    cur.close()
    conn.close()

def search_similar(embedding: list[float], top_k: int = 5):
    conn = get_conn()
    cur = conn.cursor()
    cur.execute(
        """
        SELECT source_path, content, 1 - (embedding <=> %s::vector) AS similarity
        FROM documents
        ORDER BY embedding <=> %s::vector
        LIMIT %s
        """,
        (embedding, embedding, top_k),
    )
    rows = cur.fetchall()
    cur.close()
    conn.close()
    return [{"source": r[0], "content": r[1], "similarity": r[2]} for r in rows]