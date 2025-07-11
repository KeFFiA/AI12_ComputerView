import pytesseract
from pdf2image import convert_from_path
import tempfile
import os


def extract_with_ocr(pdf_path):
    """
    Выполняет OCR для всего PDF-документа.
    Возвращает {'text': ..., 'tables': []} — таблицы из OCR не извлекаются, только текст.
    """
    extracted = {"text": "", "tables": []}

    try:
        with tempfile.TemporaryDirectory() as temp_dir:
            images = convert_from_path(pdf_path, dpi=300, output_folder=temp_dir, fmt="jpeg")
            ocr_text = []
            for i, img in enumerate(images):
                print(f"[OCR] Обрабатываем страницу {i+1}/{len(images)}")
                text = pytesseract.image_to_string(img, lang="eng")
                ocr_text.append(text)
            extracted["text"] = "\n".join(ocr_text)
    except Exception as e:
        print(f"[ERROR] Ошибка при OCR: {e}")

    return extracted
