import re
from datetime import datetime
from typing import Optional
from .ner import extract_entities

from .event_classifier import extract_events


def normalize_date(text: str) -> Optional[str]:
    patterns = [r"\b\d{1,2} [A-Z][a-z]+ \d{4}\b", r"\b\d{2}/\d{2}/\d{4}\b", r"\b\d{4}-\d{2}-\d{2}\b"]
    for pat in patterns:
        match = re.search(pat, text)
        if match:
            try:
                return str(datetime.strptime(match.group(), "%d %B %Y").date())
            except:
                try:
                    return str(datetime.strptime(match.group(), "%d/%m/%Y").date())
                except:
                    return match.group()
    return None

def normalize_money(text: str) -> Optional[float]:
    match = re.search(r"\$?USD?\s?([0-9,]+\.\d{2})", text, re.IGNORECASE)
    if match:
        return float(match.group(1).replace(",", ""))
    return None

def extract_aircraft_info(text: str) -> dict:
    return {
        "type": re.search(r"Boeing \d+ Max \d|Airbus \w+", text) and re.search(r"Boeing \d+ Max \d|Airbus \w+", text).group(),
        "registration": re.search(r"\b[A-Z0-9\-]{5,10}\b", text) and re.search(r"\b[A-Z0-9\-]{5,10}\b", text).group(),
        "serial_number": re.search(r"\b\d{5,}\b", text) and re.search(r"\b\d{5,}\b", text).group()
    }

# def normalize_answer(answer: str) -> dict:
#     return {
#         "incident_date": normalize_date(answer),
#         "location": re.search(r"(Palma de Mallorca|Athens|Madrid|London|Greece|Spain)", answer) and re.search(r"(Palma de Mallorca|Athens|Madrid|London|Greece|Spain)", answer).group(),
#         "event": re.search(r"(engine surge|bird strike|collision|fire|damage)", answer, re.IGNORECASE) and re.search(r"(engine surge|bird strike|collision|fire|damage)", answer, re.IGNORECASE).group(),
#         "aircraft": extract_aircraft_info(answer),
#         "claim": {
#             "claimed": normalize_money(answer),
#             "deductible": normalize_money(answer.split("deductible")[1]) if "deductible" in answer else None,
#             "net_paid": normalize_money(answer.split("net")[1]) if "net" in answer else None,
#             "currency": "USD"
#         },
#         "parties": {
#             "insured": re.search(r"(SMARTLYNX AIRLINES|AVION EXPRESS|Chapman Freeborn)", answer, re.IGNORECASE) and re.search(r"(SMARTLYNX AIRLINES|AVION EXPRESS|Chapman Freeborn)", answer, re.IGNORECASE).group(),
#             "insurer": re.search(r"(Howden UK Group|ADNIC|Sedgwick|Lloyds)", answer) and re.search(r"(Howden UK Group|ADNIC|Sedgwick|Lloyds)", answer).group()
#         }
#     }

def normalize_answer(text: str) -> dict:
    ner = extract_entities(text)

    # Фильтрация организаций
    insured = [org for org in ner.get("ORG", []) if "AIRLINES" in org.upper()]
    insurer = [org for org in ner.get("ORG", []) if any(x in org.upper() for x in ["HOWDEN", "INSURANCE", "SEDGWICK", "ADNIC"])]

    # Парсим деньги
    money_values = []
    for m in ner.get("MONEY", []):
        try:
            m_clean = m.replace(",", "").replace("USD", "").replace("$", "").strip()
            money_values.append(float(m_clean))
        except:
            continue

    return {
        "incident_date": ner["DATE"][0] if ner.get("DATE") else None,
        "locations": ner.get("LOC", []),
        "events": extract_events(text),
        "aircraft": extract_aircraft_info(text),
        "claim": {
            "amounts": money_values,
            "currency": "USD"
        },
        "parties": {
            "insured": insured,
            "insurer": insurer
        }
    }