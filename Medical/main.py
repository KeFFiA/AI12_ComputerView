import os
import glob
from parser.extractor_pdfplumber import extract_from_pdf
from parser.extractor_ocr import extract_with_ocr
from parser.match_fields import match_and_fill_template

from openpyxl import load_workbook

INPUT_DIR = "data/input_pdfs"
TEMPLATE_PATH = "data/template.xlsx"
OUTPUT_PATH = "output/final_result.xlsx"


def process_all_pdfs():
    print("[INFO] Загрузка шаблона Excel...")
    wb = load_workbook(TEMPLATE_PATH)
    sheet = wb.active

    pdf_files = sorted(glob.glob(os.path.join(INPUT_DIR, "*.pdf")))
    print(f"[INFO] Найдено {len(pdf_files)} PDF-файлов")

    for pdf_path in pdf_files:
        company_name = os.path.splitext(os.path.basename(pdf_path))[0]
        print(f"\n[INFO] Обработка файла: {company_name}")

        # Сначала пробуем pdfplumber
        extracted_data = extract_from_pdf(pdf_path)

        # Если данных слишком мало — пробуем OCR
        if not extracted_data or len(extracted_data.get("text", "")) < 100:
            print("[WARN] Недостаточно данных. Пробуем OCR...")
            extracted_data = extract_with_ocr(pdf_path)

        # Сопоставляем и заполняем шаблон
        match_and_fill_template(sheet, extracted_data, company_name)

    print("[INFO] Сохранение результата...")
    wb.save(OUTPUT_PATH)
    print(f"[SUCCESS] Финальный файл сохранен как {OUTPUT_PATH}")


if __name__ == "__main__":
    process_all_pdfs()
