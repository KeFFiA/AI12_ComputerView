import pdfplumber


def format_table_as_markdown(table):
    def fmt_row(row):
        return "| " + " | ".join(cell or "" for cell in row) + " |"

    if not table or len(table) < 2:
        return ""

    header = fmt_row(table[0])
    separator = "| " + " | ".join("---" for _ in table[0]) + " |"
    body = "\n".join(fmt_row(row) for row in table[1:])
    return "\n".join([header, separator, body])


def extract_from_pdf(pdf_path):
    """
    Извлекает текст и таблицы из PDF через pdfplumber.
    Возвращает словарь с полями 'text' и 'tables'.
    Вставляет маркер в текст на месте извлечения таблицы.
    """
    extracted = {"text": "", "tables": []}
    try:
        with pdfplumber.open(pdf_path) as pdf:
            full_text = []
            table_counter = 1
            for page_num, page in enumerate(pdf.pages):
                page_text_parts = []

                # Извлечение текста
                text = page.extract_text()
                if text:
                    page_text_parts.append(text)

                # Извлечение таблиц
                tables = page.extract_tables()
                for tbl in tables:
                    if tbl and len(tbl) > 1:
                        extracted["tables"].append(format_table_as_markdown(tbl))
                        page_text_parts.append(f"\n[TABLE EXTRACTED — table #{table_counter}]\n")
                        table_counter += 1

                full_text.append("\n".join(page_text_parts))

            extracted["text"] = "\n".join(full_text)
    except Exception as e:
        print(f"[ERROR] Ошибка при парсинге PDF через pdfplumber: {e}")
    return extracted
