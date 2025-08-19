import glob
import os

from pydantic import ValidationError

from loaders.pdf_loader import load_pdf_text
from chains.extract_chain import extract_information
from chains.match_template_chain import match_template
from chains.summarize_chain import compare_data
from chains.enrich_chain import enrich_cause
from db.models import save_to_db
from chains.templates.templates import Claim
from chains.create_excel import create_excel

INPUT_DIR = r"/Apps/Claims/data/input_pdfs"
PROMPT_TEMPLATE_JSON = "Transform and map the provided JSON into the structure I need.\n{format_instructions}\n{text}\n\n **IMPORTANT: JSON SCHEMA AND VALID FIELD NAMES****YOU CAN ANALYZE AND SUGGEST THE FIELD MAPPING YOURSELF, BUT DON'T MAKE UP ANYTHING OR MAKE ANY COMMENTS**"

def process_pdf(file_path):
    # raw_text = load_pdf_text(file_path)
    # extracted = extract_information(raw_text)
    extracted = {
    "report_type": "First Advice",
    "msn": None,
    "aircraft": "Airbus A320-251N",
    "registration": "TF-PPF",
    "insured": "Fly Play",
    "insurer": "Starr Underwriting Agents Limited",
    "cause": "No. 2 engine Thrust Reverser damaged during installation",
    "location": "Montpellier–Méditerranée Airport, France",
    "dol": "2025-03-26",
    "indemnity_reserve": None,
    "indemnity_reserve_currency": None,
    "paid_to_date": 8000.0,
    "paid_to_date_currency": "GBP",
    "summary": "FlyPlay, Airbus A320-251N, Registration TF-PPF, No. 2 engine Thrust Reverser damaged during installation at Montpellier-Méditerranée Airport, France on 26 March 2025. The aircraft was undergoing scheduled maintenance at the Vallair facility. Following damage being sustained by Vallair to the original installed Thrust Reverser (which is being handled as a separate claim), a replacement Thrust Reverser was procured by FlyPlay and shipped to Vallair for installation. During the installation process undertaken by Vallair employees, which involved the Thrust Reverser being lifted in a sling by crane, it came into contact with the No. 6 strut installed on engine No. 2. Preliminary inspections revealed impact deformation to the inner fixed structure, outside of allowable limitations for continued operation. After undertaking detailed damage mapping, the Thrust Reverser was repaired in accordance with the Structural Repair Manual (SRM) by Vallair. McLarens Paris office was able to undertake a survey at the Vallair facility and discuss the extent of the damage sustained and repairs undertaken.",
    "contact_name": "Gary Clift",
    "contact_title": "Aviation Claims Manager",
    "contact_phone": "+44 (0)788 580 3530",
    "contact_email": "gary.clift@mclarens.com"
}
    try:
        Claim(**extracted)
    except ValidationError:
        extracted = extract_information(text=extracted, template=PROMPT_TEMPLATE_JSON)
    summarized = compare_data(extracted)
    # enriched = enrich_cause(summarized)
    print("\n\n", summarized)
    # save_to_db(enriched)
    # print(enriched)
    # filename = create_excel(extracted)


def start():
    pdf_files = sorted(glob.glob(os.path.join(INPUT_DIR, "*.pdf")))
    print(f"[INFO] Найдено {len(pdf_files)} PDF-файлов")

    for pdf_path in pdf_files:
        company_name = os.path.splitext(os.path.basename(pdf_path))[0]
        print(f"\n[INFO] Обработка файла: {company_name}")
        process_pdf(file_path=pdf_path)

if __name__ == "__main__":
    # start()
    process_pdf(r"/Apps/Claims/data/input_pdfs\25-03-20 AGB.165439 Final Report-11560-80733383.pdf")
    # process_pdf(r"D:\PycharmProjects\ASG_ComputerView\Apps\Claims\data\input_pdfs\25-03-21 AGB.166646 Interim Report No. 1-11560-80778858.PDF")
    # process_pdf(r"D:\PycharmProjects\ASG_ComputerView\Apps\Claims\data\input_pdfs\20250304.SAS.REPORT4.10157988.HAR.HOWDEN.pdf")
    # process_pdf(r"D:\PycharmProjects\ASG_ComputerView\Apps\Claims\data\input_pdfs\20250321.SAS.REPORT 6.10170261.HOWDEN.pdf")
    #
    # process_pdf(r"D:\PycharmProjects\ASG_ComputerView\Apps\Claims\data\input_pdfs\24-08-23 AGB.166536 Full and Final Insurance Release.pdf")
    # process_pdf(r"D:\PycharmProjects\ASG_ComputerView\Apps\Claims\data\input_pdfs\20250311.SAS.REPORT3.10222675.HOWDEN.pdf")


