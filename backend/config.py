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

# LangSmith Observability Configuration
LANGCHAIN_TRACING_V2 = os.getenv("LANGCHAIN_TRACING_V2", "false")
LANGCHAIN_API_KEY = os.getenv("LANGCHAIN_API_KEY", "")
LANGCHAIN_PROJECT = os.getenv("LANGCHAIN_PROJECT", "sovereign-ai-workbench")
LANGCHAIN_ENDPOINT = os.getenv("LANGCHAIN_ENDPOINT", "https://api.smith.langchain.com")

if LANGCHAIN_TRACING_V2.lower() in ("true", "1") and LANGCHAIN_API_KEY:
    os.environ["LANGCHAIN_TRACING_V2"] = "true"
    os.environ["LANGCHAIN_API_KEY"] = LANGCHAIN_API_KEY
    os.environ["LANGCHAIN_PROJECT"] = LANGCHAIN_PROJECT
    os.environ["LANGCHAIN_ENDPOINT"] = LANGCHAIN_ENDPOINT

ALLOWED_OUTBOUND_HOSTS = {"postgres", "host.docker.internal"}

if LANGCHAIN_TRACING_V2.lower() in ("true", "1") or LANGCHAIN_API_KEY:
    from urllib.parse import urlparse
    parsed = urlparse(LANGCHAIN_ENDPOINT)
    if parsed.hostname:
        ALLOWED_OUTBOUND_HOSTS.add(parsed.hostname)
    ALLOWED_OUTBOUND_HOSTS.add("api.smith.langchain.com")
    ALLOWED_OUTBOUND_HOSTS.add("smith.langchain.com")