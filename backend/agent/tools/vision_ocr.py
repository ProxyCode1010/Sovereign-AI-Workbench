import base64
import fitz
import pytesseract
from PIL import Image
import io
from model_router import call_ollama
from config import VISION_MODEL

def pdf_page_to_image_b64(pdf_path: str, page_num: int = 0) -> str:
    doc = fitz.open(pdf_path)
    page = doc[page_num]
    pix = page.get_pixmap(dpi=150)
    img_bytes = pix.tobytes("png")
    doc.close()
    return base64.b64encode(img_bytes).decode("utf-8")

def image_file_to_b64(path: str) -> str:
    with open(path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")

def tesseract_ocr(image_b64: str) -> str:
    img_bytes = base64.b64decode(image_b64)
    img = Image.open(io.BytesIO(img_bytes))
    return pytesseract.image_to_string(img)

def vision_describe(image_b64: str, prompt: str) -> str:
    """Use moondream for understanding scanned drawings / handwritten notes / photos."""
    return call_ollama(VISION_MODEL, prompt, images=[image_b64])

def analyze_scanned_document(path: str, instruction: str) -> dict:
    """Combines raw OCR text + vision-model reasoning for best accuracy on scans."""
    if path.lower().endswith(".pdf"):
        img_b64 = pdf_page_to_image_b64(path, 0)
    else:
        img_b64 = image_file_to_b64(path)

    raw_ocr = tesseract_ocr(img_b64)
    vision_summary = vision_describe(
        img_b64,
        f"{instruction}\n\nRaw OCR text extracted (may contain errors):\n{raw_ocr}"
    )
    return {"raw_ocr": raw_ocr, "vision_summary": vision_summary}