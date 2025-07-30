import json
import os
import glob

from ResponseModel import InsurancesResponse
from parser.extractor_pdfplumber import extract_from_pdf
from parser.extractor_ocr import extract_with_ocr
from openai import OpenAI
from openpyxl import load_workbook


test = {
  "Company Name": "",
  "Insurance Category": "",
  "Number of Lives": 0,
  "Area of Coverage": "",
  "Extended Territory for Emergency Treatment Only": "",
  "Annual Aggregate Limit": "",
  "Pre-existing Conditions": "",
  "Network Type": "",
  "OP Consultation": "",
  "OP Physiotherapy": "",
  "Pharmaceuticals": "",
  "Diagnostics": "",
  "Dental Benefit": "",
  "Optical Benefit": "",
  "Alternative Medicines": "",
  "Maternity OP Benefit": "",
  "Psychiatric OP Benefit": "",
  "Outside Network Co-Insurance": "",
  "IP Benefit": "",
  "Maternity IP Benefit": "",
  "Psychiatric IP Benefit": "",
  "Organ Transplant": "",
  "In-patient Cash Benefit": "",
  "Annual Health Check-up": "",
  "Value-Added Services": "",
  "Gross Premium (including VAT & Basmah)": "",
  "Cost Per Member": ""
}


INPUT_DIR = "data/input_pdfs_med"
TEMPLATE_PATH = "data/template.xlsx"
OUTPUT_PATH = "output/med/final_result.xlsx"

client = OpenAI(base_url="http://212.69.84.131:8000", api_key="llama")

def extract_info(content: str):
    # делаем запрос к API
    response = client.chat.completions.parse(
        model="Meta-Llama-3-8B-Instruct",
        messages=[
            # {
            #     "role": "system",
            #     "content": (
            #         "You are a strict insurance data extractor. "
            #         "Extract only factual and structured information as per the schema below. "
            #         "Do NOT hallucinate or guess missing fields. If a field is missing, skip the record. "
            #         "Return your response as a valid JSON object in the following structure:\n\n"
            #         "{ \"insurances\": [ { <Insurance Fields> } ] }\n\n"
            #         "Fields include: Company Name, Insurance Category, Number of Lives, Area of Coverage or Geographical Scope, "
            #         "Extended Territory for Emergency Treatment Only, Annual Aggregate Limit, Pre-existing Conditions, "
            #         "Network Type, OP Consultation, OP Physiotherapy, Pharmaceuticals, Diagnostics, Dental Benefit, "
            #         "Optical Benefit, Alternative Medicines, Maternity OP Benefit, Psychiatric OP Benefit, "
            #         "Outside Network Co-Insurance, IP Benefit, Maternity IP Benefit, Psychiatric IP Benefit, "
            #         "Organ Transplant (including donor charges but excluding cost of organ), "
            #         "In-patient Cash Benefit (if free treatment taken at a government facility in UAE), "
            #         "Annual Health Check-up, Value-Added Services, Gross Premium (including VAT & Basmah), Cost Per Member."
            #     ),
            # },
            {
                "role": "user",
                "content": f"""
                You are a professional insurance assistant. Extract the following information from the insurance document.

Return STRICTLY a JSON object with these fields:

[{test}]

Use the following document section as input:
---
{json.dumps(content)}
---
                """
            }
        ],
        response_format=InsurancesResponse,
        temperature=0.4,

    )

    # возвращаем ответ
    return response.choices[0].message.content

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
        if not extracted_data:
            print("[WARN] Недостаточно данных. Пробуем OCR...")
            extracted_data = extract_with_ocr(pdf_path)

        print("extracted data: \n", extracted_data)
        json_text = extract_info(content=extracted_data)
        print("extracted info: \n", json_text)



    print("[INFO] Сохранение результата...")
    wb.save(OUTPUT_PATH)
    print(f"[SUCCESS] Финальный файл сохранен как {OUTPUT_PATH}")


if __name__ == "__main__":
    process_all_pdfs()
