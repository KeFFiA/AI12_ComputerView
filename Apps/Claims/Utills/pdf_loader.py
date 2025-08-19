from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfReader

from Config import setup_logger

logger = setup_logger(__name__)

def load_pdf_text(path: str) -> str:
    try:
        logger.info("Trying to extract PDF text...")
        reader = PdfReader(path)
        text = ''.join(page.extract_text() or '' for page in reader.pages)
        if len(text.strip()) > 50:
            logger.info(f"Extraction completed. Extracted {len(reader.pages)} pages")
            return text
        raise
    except:
        logger.exception("Extract PDF text failed")
        pass

    logger.info("Using OCR...")
    images = convert_from_path(path)
    text = ''.join(pytesseract.image_to_string(img) for img in images)
    return text

