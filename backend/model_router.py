import requests
from config import OLLAMA_HOST, GENERAL_MODEL, CODE_MODEL, VISION_MODEL

CODE_KEYWORDS = ["code", "script", "function", "python", "bug", "debug", "sql", "program", "compile", "algorithm"]
VISION_KEYWORDS = ["image", "photo", "scan", "drawing", "diagram", "picture", "ocr"]
QUESTION_STARTERS = ("what", "who", "when", "where", "why", "how", "is ", "does", "can ", "explain", "list", "give me")

MODEL_MAP = {
    "general": GENERAL_MODEL,
    "code": CODE_MODEL,
    "vision": VISION_MODEL,
}

CLASSIFIER_SYSTEM = """You classify a single user request into exactly one word: code, vision, or general.

Rules:
- "code" = the user wants you to WRITE, DEBUG, or FIX a computer program/script/function.
- "vision" = the request is about reading or understanding an image, photo, scan, or drawing.
- "general" = everything else: questions, explanations, summaries, SOPs, procedures, definitions, how-to steps that are NOT about writing code.

Examples:
"What is the SOP for valve isolation?" -> general
"Write a python function to sort a list" -> code
"My calculation script has a bug, fix it" -> code
"Summarize this inspection report" -> general
"What does this scanned drawing show?" -> vision

Respond with ONLY the single word: code, vision, or general."""


def keyword_classify(task_text: str) -> str | None:
    """Fast path — returns a category if there's a confident, unambiguous signal."""
    t = task_text.lower().strip()

    if any(k in t for k in VISION_KEYWORDS):
        return "vision"

    # Questions ("What is...", "How do I...") are almost never code-writing requests,
    # even if they happen to contain a code-ish word somewhere in them.
    if t.startswith(QUESTION_STARTERS) and not any(k in t for k in CODE_KEYWORDS):
        return "general"

    if any(k in t for k in CODE_KEYWORDS):
        return "code"

    return None


def llm_classify(task_text: str) -> str:
    """Slow path — asks the general model itself to decide, for genuinely ambiguous queries."""
    try:
        resp = requests.post(
            f"{OLLAMA_HOST}/api/generate",
            json={
                "model": GENERAL_MODEL,
                "prompt": f'Classify this request: "{task_text}"',
                "system": CLASSIFIER_SYSTEM,
                "stream": False,
                "keep_alive": "2m",
                "options": {"temperature": 0},
            },
            timeout=30,
        )
        resp.raise_for_status()
        raw = resp.json()["response"].strip().lower()
        for kind in ("code", "vision", "general"):
            if raw == kind or raw.startswith(kind) or f" {kind}" in raw:
                return kind
    except Exception as e:
        print(f"[ROUTER] LLM classification failed, defaulting to general: {e}")
    return "general"


def classify_task(task_text: str, has_image: bool = False) -> tuple[str, str]:
    """Returns (category, method) where method is 'image_flag' | 'keyword' | 'llm_agent'."""
    if has_image:
        return "vision", "image_flag"

    kw_result = keyword_classify(task_text)
    if kw_result:
        return kw_result, "keyword"

    llm_result = llm_classify(task_text)
    return llm_result, "llm_agent"


def get_model_for_task(task_text: str, has_image: bool = False):
    kind, method = classify_task(task_text, has_image)
    model = MODEL_MAP[kind]
    print(f"[ROUTER] method={method} | task='{task_text[:60]}' -> category='{kind}' -> model='{model}'")
    return model, kind


def call_ollama(model: str, prompt: str, images: list = None, system: str = None) -> str:
    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False,
        "keep_alive": "2m",
    }
    if system:
        payload["system"] = system
    if images:
        payload["images"] = images

    resp = requests.post(f"{OLLAMA_HOST}/api/generate", json=payload, timeout=300)
    resp.raise_for_status()
    return resp.json()["response"]