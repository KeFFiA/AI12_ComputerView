

PROMPT_TEMPLATE_JSON = "Transform and map the provided JSON into the structure I need.\n{format_instructions}\n{text}\n\n **IMPORTANT: JSON SCHEMA AND VALID FIELD NAMES****YOU CAN ANALYZE AND SUGGEST THE FIELD MAPPING YOURSELF, BUT DON'T MAKE UP ANYTHING OR MAKE ANY COMMENTS**"
MAINEXTRACT_PROMPT = "Extract all possible information from this text.\n{format_instructions}\n{text}\n\n **IMPORTANT: JSON SCHEMA**"

AIRCRAFT_PROMPT = """
You are given JSON: {data}.
For each key, find the most similar values from the DB using the available tools.
If the fields are related (for example, registration and msn), use SearchAircraft(you can use registration or msn field) to replace both.
Return the result strictly in JSON format, replacing all values received from the DB.
    """
