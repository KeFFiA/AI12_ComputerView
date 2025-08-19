import json
import pandas as pd
from datetime import datetime

FOLDER_PATH = r"D:\PycharmProjects\ASG_ComputerView\Apps\Claims\output\\"

def create_excel(data: dict):
    df = pd.DataFrame([data])
    filename = FOLDER_PATH + datetime.now().strftime("%Y-%m-%d_%H-%M-%S") + ".xlsx"
    df.to_excel(filename, index=False)

    print(f"Файл сохранён: {filename}")
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
    create_excel(data=test)