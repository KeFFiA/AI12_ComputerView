from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfReader

def load_pdf_text(path: str) -> str:
    try:
        reader = PdfReader(path)
        text = ''.join(page.extract_text() or '' for page in reader.pages)
        if text.strip():
            # print('\n\n\n', text, '\n\n\n')
            return text
    except:
        pass

    images = convert_from_path(path)
    text = ''.join(pytesseract.image_to_string(img) for img in images)
    # print('\n\n\n', text, '\n\n\n')
    return text

