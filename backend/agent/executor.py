from agent.tools.rag_search import rag_search
from agent.tools.file_tools import read_file, write_output_file
from agent.tools.vision_ocr import analyze_scanned_document
from agent.tools.code_sandbox import run_code_in_sandbox
from agent.tools.docx_writer import create_approval_note
from agent.tools.xlsx_writer import create_calculation_sheet
from agent.tools.pptx_writer import create_slide_deck
from model_router import call_ollama, get_model_for_task, classify_task


def execute_inspection_to_approval_note(scan_path: str, note_title: str) -> dict:
    """End-to-end demo flow: scanned inspection report -> approval note (docx)."""
    from config import VISION_MODEL

    analysis = analyze_scanned_document(
        scan_path,
        "Extract key findings, defects, measurements, and any recommendation from this inspection report."
    )

    ocr_text = analysis["raw_ocr"].strip()
    structuring_model, _ = get_model_for_task("summarize findings")

    if len(ocr_text) > 30:
        source_text = ocr_text
    else:
        source_text = analysis["vision_summary"]

    structuring_prompt = f"""Below is text extracted from a scanned inspection report. Use ONLY the information present in this text — do not invent dates, names, or findings that are not written here.

TEXT:
{source_text}

List each finding from the report as one line per finding, then on a final new line starting with 'RECOMMENDATION:' give the recommendation exactly as stated in the text. If no recommendation is stated, write 'RECOMMENDATION: Refer to engineering team for further review.'"""

    structured = call_ollama(structuring_model, structuring_prompt)

    findings = []
    recommendation = ""
    for line in structured.splitlines():
        line = line.strip("-#* ").strip()
        if not line:
            continue
        if line.upper().startswith("RECOMMENDATION"):
            recommendation = line.split(":", 1)[-1].strip()
        elif not line.upper().startswith("KEY FINDING"):
            findings.append(line)

    if not recommendation:
        recommendation = "Refer to engineering team for further review."

    path = create_approval_note("approval_note.docx", note_title, findings, recommendation)
    return {
        "analysis": analysis,
        "findings": findings,
        "recommendation": recommendation,
        "output_file": path,
        "model_used": f"{VISION_MODEL} (image reading) + {structuring_model} (structuring)",
        "routing_category": "vision",
        "routing_method": "image_flag",
    }

def execute_coding_task(task_description: str) -> dict:
    """End-to-end demo flow: code request -> generated code -> run in sandbox -> verified output."""
    category, method = classify_task(task_description)
    model, kind = get_model_for_task(task_description)

    code_prompt = (
        "Write a complete, runnable Python script for this task.\n"
        "Output ONLY raw Python code. No explanations. No markdown. "
        "No text before or after the code.\n\n"
        f"Task: {task_description}"
    )
    raw = call_ollama(model, code_prompt)

    code = raw.strip()
    if "```" in code:
        parts = code.split("```")
        for part in parts:
            part = part.strip()
            if part.startswith("python"):
                part = part[len("python"):].strip()
            if part and ("def " in part or "import " in part or "print(" in part):
                code = part
                break
    else:
        lines = code.splitlines()
        cutoff = len(lines)
        for i, line in enumerate(lines):
            stripped = line.strip()
            if stripped and not stripped.startswith((
                "#", "import", "from", "def", "class", "print", "    ", "\t",
                "return", "if", "for", "while", "with", "try", "except", "else", "elif"
            )) and "=" not in stripped and "(" not in stripped:
                cutoff = i
                break
        code = "\n".join(lines[:cutoff]).strip()

    result = run_code_in_sandbox(code)
    return {
        "model_used": model,
        "routing_category": kind,
        "routing_method": method,
        "code": code,
        "sandbox_result": result,
    }


def execute_rag_query(question: str) -> dict:
    """End-to-end demo flow: grounded Q&A against internal SOPs/manuals."""
    category, method = classify_task(question)

    hits = rag_search(question, top_k=4)
    context = "\n\n".join(f"[{h['source']}] {h['content']}" for h in hits)
    model, kind = get_model_for_task(question)
    prompt = f"""Answer using ONLY the context below. If not found, say so.

Context:
{context}

Question: {question}"""
    answer = call_ollama(model, prompt)
    return {
        "answer": answer,
        "sources": [h["source"] for h in hits],
        "model_used": model,
        "routing_category": kind,
        "routing_method": method,
    }