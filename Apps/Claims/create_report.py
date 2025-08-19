import json
from datetime import datetime
from pathlib import Path

from Config import setup_logger

FOLDER_PATH = Path("data/output_claims")
logger = setup_logger(__name__)

FOLDER_PATH.mkdir(parents=True, exist_ok=True)

def create_report(data: dict):

    filename = FOLDER_PATH / f"{datetime.now().strftime('%Y-%m-%d_%H-%M-%S')}.json"
    with open(filename, "w", encoding="utf-8") as file:
        file.write(json.dumps(data, indent=4))

    logger.info(f"File saved: {filename}")
    return filename


if __name__ == "__main__":
    test = {
    "report_type": "SETTLEMENT",
    "msn": 10157988,
    "aircraft": "Airbus A320",
    "registration": "LY-MLF",
    "insured": "Avion Express Malta Ltd.",
    "insurer": "Underwriters at Risk per Howden",
    "cause": "LH engine surge during test at Athens, Greece",
    "location": "Aegean MRO, Athens, Greece",
    "dol": "2022-07-04",
    "indemnity_reserve": 1618146.68,
    "indemnity_reserve_currency": "USD",
    "paid_to_date": 1615485.0,
    "paid_to_date_currency": "USD",
    "summary": "The final repair cost summary and supporting documentation have been reviewed and adjusted accordingly, presenting the following settlement report for Underwriters' consideration.",
    "contact_name": "Sam Edwards",
    "contact_title": "Senior Surveyor & Adjuster – Aviation",
    "contact_phone": "+44 7795666031",
    "contact_email": "sam.edwards@sedgwick.com"
}
    create_report(data=test)