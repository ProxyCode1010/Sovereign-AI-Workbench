import os

DATABASE_URL = os.getenv("DATABASE_URL", "postgresql://sw_user:sw_pass@postgres:5432/sovereign_workbench")
OLLAMA_HOST = os.getenv("OLLAMA_HOST", "http://ollama:11434")

GENERAL_MODEL = os.getenv("GENERAL_MODEL", "qwen2.5:1.5b-instruct")
CODE_MODEL = os.getenv("CODE_MODEL", "qwen2.5-coder:1.5b")
VISION_MODEL = os.getenv("VISION_MODEL", "moondream:1.8b")
EMBED_MODEL = os.getenv("EMBED_MODEL", "nomic-embed-text")

SANDBOX_IMAGE = os.getenv("SANDBOX_IMAGE", "sw_sandbox:latest")

UPLOAD_DIR = "/app/data/uploads"
OUTPUT_DIR = "/app/data/outputs"
KB_DIR = "/app/data/knowledge_base"

ALLOWED_OUTBOUND_HOSTS = {"postgres", "host.docker.internal"}