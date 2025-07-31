import re
from datetime import datetime
from typing import Optional, Tuple
from .ner import extract_entities

from .event_classifier import extract_events


def extract_labeled_amount(text: str, label: str) -> Optional[Tuple[str, float]]:
    """
    Ищет строку вроде 'CLAIMED AMOUNT USD 123,456.78' и возвращает кортеж ('USD', 123456.78)
    """
    pattern = rf"{re.escape(label)}\s+([A-Z]{{3}}|\$|€|£|¥)?\s?([\d,]+\.\d{{2}})"
    match = re.search(pattern, text, re.IGNORECASE)
    if match:
        currency = match.group(1).strip().upper() if match.group(1) else "UNKNOWN"
        amount = float(match.group(2).replace(",", ""))
        return currency, amount
    return None

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

def normalize_money_all(text: str) -> list[tuple[str, float]]:
    # Поддержка стандартных валют и знаков
    pattern = r'(?P<currency>[A-Z]{3}|[$€£¥])[\s]?(?P<amount>\d{1,3}(?:,\d{3})*(?:\.\d{2})?)'
    results = []

    for match in re.finditer(pattern, text):
        currency = match.group("currency").upper()
        amount = float(match.group("amount").replace(",", ""))
        results.append((currency, amount))

    return results


def normalize_answer(text: str) -> dict:
    ner = extract_entities(text)

    # Фильтрация организаций
    insured = [org for org in ner.get("ORG", []) if "AIRLINES" in org.upper()]
    insurer = [org for org in ner.get("ORG", []) if any(x in org.upper() for x in ["HOWDEN", "INSURANCE", "SEDGWICK", "ADNIC"])]

    # Все суммы (в свободном тексте)
    money_values = normalize_money_all(text)

    # Статьи расходов
    claimed = extract_labeled_amount(text, "CLAIMED AMOUNT")
    deductible = extract_labeled_amount(text, "LESS APPLICABLE DEDUCTIBLE")
    net_paid = extract_labeled_amount(text, "NET CLAIMED AMOUNT")

    claim = {
        "amounts": [{"currency": cur, "value": val} for cur, val in money_values],
        "claimed": {"currency": claimed[0], "value": claimed[1]} if claimed else None,
        "deductible": {"currency": deductible[0], "value": deductible[1]} if deductible else None,
        "net_paid": {"currency": net_paid[0], "value": net_paid[1]} if net_paid else None
    }

    return {
        "incident_date": ner["DATE"][0] if ner.get("DATE") else None,
        "locations": ner.get("LOC", []),
        "events": extract_events(text),
        "aircraft": extract_aircraft_info(text),
        "claim": claim,
        "parties": {
            "insured": insured,
            "insurer": insurer
        }
    }
