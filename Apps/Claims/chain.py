from pydantic import ValidationError

from create_report import create_report
from Config import PROMPT_TEMPLATE_JSON, setup_logger
from summarize_chain import compare_data
from Config.Templates import Claim
from extract_chain import extract_information
from Utills.pdf_loader import load_pdf_text

logger = setup_logger(__name__)

def process_pdf(file_path, filename):
    try:
        logger.info("Stage 1. Extract text from PDF")
        raw_text = load_pdf_text(file_path)
        logger.info("Stage 2. Extract JSON from extracted raw text")
        extracted = extract_information(raw_text)
        logger.info("Stage 3. Valid extracted JSON")
        try:
            Claim(**extracted)
            logger.info("Valid")
        except ValidationError:
            logger.error("Validation Error. Trying to validate")
            extracted = extract_information(text=extracted, template=PROMPT_TEMPLATE_JSON)
        logger.info("Stage 4. Compare JSON fields with DB")
        compared = compare_data(extracted)
        # enriched = enrich_cause(summarized)
        # save_to_db(enriched)
        # print(enriched)
        filename = create_report(compared, filename)
        return True
    except Exception as e:
        # TODO: logger
        return False


    #     extracted = {
    #     "report_type": "First Advice",
    #     "msn": None,
    #     "aircraft": "Airbus A320-251N",
    #     "registration": "TF-PPF",
    #     "insured": "Fly Play",
    #     "insurer": "Starr Underwriting Agents Limited",
    #     "cause": "No. 2 engine Thrust Reverser damaged during installation",
    #     "location": "Montpellier–Méditerranée Airport, France",
    #     "dol": "2025-03-26",
    #     "indemnity_reserve": None,
    #     "indemnity_reserve_currency": None,
    #     "paid_to_date": 8000.0,
    #     "paid_to_date_currency": "GBP",
    #     "summary": "FlyPlay, Airbus A320-251N, Registration TF-PPF, No. 2 engine Thrust Reverser damaged during installation at Montpellier-Méditerranée Airport, France on 26 March 2025. The aircraft was undergoing scheduled maintenance at the Vallair facility. Following damage being sustained by Vallair to the original installed Thrust Reverser (which is being handled as a separate claim), a replacement Thrust Reverser was procured by FlyPlay and shipped to Vallair for installation. During the installation process undertaken by Vallair employees, which involved the Thrust Reverser being lifted in a sling by crane, it came into contact with the No. 6 strut installed on engine No. 2. Preliminary inspections revealed impact deformation to the inner fixed structure, outside of allowable limitations for continued operation. After undertaking detailed damage mapping, the Thrust Reverser was repaired in accordance with the Structural Repair Manual (SRM) by Vallair. McLarens Paris office was able to undertake a survey at the Vallair facility and discuss the extent of the damage sustained and repairs undertaken.",
    #     "contact_name": "Gary Clift",
    #     "contact_title": "Aviation Claims Manager",
    #     "contact_phone": "+44 (0)788 580 3530",
    #     "contact_email": "gary.clift@mclarens.com"
    # }