import json
from model_router import call_ollama, get_model_for_task

PLANNER_SYSTEM = """You are a task planner for an industrial AI assistant.
Break the user's task into a short ordered list of steps using ONLY these tools:
- rag_search(query)
- read_file(filename)
- analyze_scanned_document(path, instruction)
- run_code_in_sandbox(code)
- create_approval_note(filename, title, findings, recommendation)
- create_calculation_sheet(filename, title, rows)
- create_slide_deck(filename, slides)

Respond ONLY with valid JSON: {"steps": [{"tool": "...", "reason": "..."}]}
Keep it to 2-5 steps. No extra text."""

def make_plan(task_text: str) -> dict:
    model, _ = get_model_for_task(task_text)
    raw = call_ollama(model, task_text, system=PLANNER_SYSTEM)
    try:
        cleaned = raw.strip().strip("`").replace("json\n", "")
        return json.loads(cleaned)
    except Exception:
        return {"steps": [{"tool": "rag_search", "reason": "fallback: unable to parse plan"}], "raw": raw}