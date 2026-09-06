CREATE EXTENSION IF NOT EXISTS vector;

CREATE TABLE IF NOT EXISTS documents (
    id SERIAL PRIMARY KEY,
    source_path TEXT NOT NULL,
    chunk_index INT NOT NULL,
    content TEXT NOT NULL,
    embedding VECTOR(768),
    created_at TIMESTAMP DEFAULT NOW()
);


CREATE TABLE IF NOT EXISTS agent_runs (
    id SERIAL PRIMARY KEY,
    task TEXT NOT NULL,
    plan JSONB,
    status TEXT DEFAULT 'running',
    result TEXT,
    created_at TIMESTAMP DEFAULT NOW()
);