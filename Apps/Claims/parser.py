import pdfplumber, pytesseract
from pdf2image import convert_from_path

def extract_text_pdf(path: str) -> str:
    text = ""
    with pdfplumber.open(path) as pdf:
        for page in pdf.pages:
            txt = page.extract_text()
            if txt:
                text += txt + "\n"
    return text.strip()

def extract_text_ocr(path: str) -> str:
    images = convert_from_path(path)
    return "\n".join(pytesseract.image_to_string(img) for img in images)

def get_pdf_text(path: str) -> str:
    text = extract_text_pdf(path)
    if not text or len(text.strip()) < 300:
        text = extract_text_ocr(path)
    return text.strip()
