import re
from rapidfuzz import fuzz, process
from Medical.parser.sentence_transformer_matcher import match_with_embeddings

# Ключевые поля из шаблона Excel
TARGET_FIELDS = [
    "KEY BENEFITS",
    "Number of Lives",
    "Area of Coverage/ Geographical Scope",
    "Extended Territory for Emergency treatment only",
    "Annual Aggregate Limit",
    "Pre-existing conditions",
    "Network Type",
    "OP Consultation",
    "OP Physiotherapy",
    "Pharmaceuticals",
    "Diagnostics",
    "Dental Benefit",
    "Optical Benefit",
    "Alternative Medicines",
    "Maternity OP Benefit",
    "Psychiatric OP benefit",
    "Outside Network Co-Insurance",
    "IP Benefit",
    "Maternity IP benefit",
    "Psychiatric IP benefit",
    "Organ Transplant",
    "In-patient cash benefit if Free of Charge treatment is taken free of charge at a Govt. Facility in UAE",
    "Annual Health check up",
    "Value Added Services",
    "Gross Premium (Incl VAT & Basmah)",
    "PREMIUM PER MEMBER"
]

FUZZY_MATCH_THRESHOLD = 80
EMBEDDING_MATCH_THRESHOLD = 0.6


def match_and_fill_template(sheet, extracted_data, company_name):
    text = extracted_data.get("text", "").lower()
    lines = text.splitlines()

    row = sheet.max_row + 1
    sheet.cell(row=row, column=1).value = company_name

    for col, field in enumerate(TARGET_FIELDS, start=2):
        found = match_field_with_fallback(field, lines)
        sheet.cell(row=row, column=col).value = found or "NOT FOUND"  # TODO: заменить "NOT FOUND" на '' если нужно пустое


def match_field_with_fallback(field, lines):
    # 1. Попробуем SentenceTransformer
    best_line, score = match_with_embeddings(field, lines)
    if score >= EMBEDDING_MATCH_THRESHOLD:
        parts = re.split(r":|\t| - ", best_line, maxsplit=1)
        if len(parts) == 2:
            return parts[1].strip()
        return best_line.strip()

    # 2. Попробуем RapidFuzz fallback
    match = process.extractOne(field, lines, scorer=fuzz.partial_ratio)
    if match:
        best_line, score, _ = match
        if score >= FUZZY_MATCH_THRESHOLD:
            parts = re.split(r":|\t| - ", best_line, maxsplit=1)
            if len(parts) == 2:
                return parts[1].strip()
            return best_line.strip()

    return None