import pdfplumber

def extract_from_pdf(pdf_path):
    """
    Извлекает текст и таблицы из PDF через pdfplumber.
    Возвращает словарь с полями 'text' и 'tables'.
    """
    extracted = {"text": "", "tables": []}
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = []
            for page_num, page in enumerate(pdf.pages):
                text = page.extract_text()
                if text:
                    full_text.append(text)

                tables = page.extract_tables()
                for tbl in tables:
                    if tbl and len(tbl) > 1:
                        extracted["tables"].append(tbl)

            extracted["text"] = "\n".join(full_text)
    except Exception as e:
        print(f"[ERROR] Ошибка при парсинге PDF через pdfplumber: {e}")
    return extracted