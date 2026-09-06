from fastapi import APIRouter, UploadFile, File, Form
import os
import shutil
from config import UPLOAD_DIR
from agent.executor import execute_inspection_to_approval_note, execute_coding_task, execute_rag_query
from rag.ingest import ingest_directory
from config import KB_DIR

router = APIRouter()

@router.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    dest = os.path.join(UPLOAD_DIR, file.filename)
    with open(dest, "wb") as f:
        shutil.copyfileobj(file.file, f)
    return {"path": dest}

@router.post("/agent/inspection-to-note")
async def inspection_to_note(scan_filename: str = Form(...), title: str = Form("Inspection Approval Note")):
    path = os.path.join(UPLOAD_DIR, scan_filename)
    result = execute_inspection_to_approval_note(path, title)
    return result

@router.post("/agent/code-task")
async def code_task(description: str = Form(...)):
    return execute_coding_task(description)

@router.post("/agent/rag-query")
async def rag_query(question: str = Form(...)):
    return execute_rag_query(question)

@router.post("/kb/ingest")
async def kb_ingest():
    results = ingest_directory(KB_DIR)
    return {"ingested": results}

@router.get("/health")
async def health():
    return {"status": "ok"}