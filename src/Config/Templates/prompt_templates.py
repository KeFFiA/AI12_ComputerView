

PROMPT_TEMPLATE_JSON = "Transform and map the provided JSON into the structure I need.\n{format_instructions}\n{text}\n\n **IMPORTANT: JSON SCHEMA AND VALID FIELD NAMES****YOU CAN ANALYZE AND SUGGEST THE FIELD MAPPING YOURSELF, BUT DON'T MAKE UP ANYTHING OR MAKE ANY COMMENTS**"
MAINEXTRACT_PROMPT = "Extract all possible information from this text.\n{format_instructions}\n{text}\n\n **IMPORTANT: JSON SCHEMA**"

AIRCRAFT_PROMPT = """
You are given JSON: {data}.
For each key, find the most similar values from the DB using the available tools.
If the fields are related (for example, registration and msn), use SearchAircraft (you can use registration or msn field) to replace both.
If the field is 'insured' (airline/company name), use SearchAirline.
Return the result strictly in JSON format, replacing all values received from the DB.
"""

FILE_TYPE_PROMPT = """
You are an expert document classifier.  
Your task is to determine which of the following three categories best matches the provided document text:

1. Lease Agreement — a legal contract for the lease of an aircraft or equipment, often containing provisions regarding the rent, term, lessor, lessee, and liabilities.
2. Payment Document — any document confirming a payment or transaction, such as an invoice, receipt, bank transfer, or payment confirmation.  
3. Insurance Surveyor Report — a document describing damage assessment, inspection results, insurance claims, or evaluations of insured assets.

Analyze the given text carefully and respond ONLY with a concise JSON object
Text to analyze:
'{text}'
            """

PAGE_NAVIGATION_PROMPT = """
You are an expert document structure analyst.  
Your task is to determine whether the provided document text contains a **page navigation section (Table of Contents)**.

A page navigation section typically includes a structured list of document sections or articles followed by corresponding page numbers.  
It often contains keywords or patterns such as:
- "CONTENTS", "TABLE OF CONTENTS", or "INDEX"
- Sequential numbering of sections (e.g., 1., 1.1., 2., 3.)
- Lines where a section title is followed by a page number (e.g., "LEASE TERM ............................................. 2")
- Multiple consecutive lines of this type before the main document body starts.

Analyze the provided text carefully and respond ONLY with a concise JSON object
Text to analyze:
'{text}'
            """



TEXT_ANALYSE_WITHOUT_PAGES_PROMPT = """
You are an expert data extraction model specialized in semantic text analysis.  
Your task is to find and extract all relevant values from the provided document text based on a given list of field names.  
These fields may appear in the text under slightly different names or synonyms (for example, "Agreed Value" ≈ "Total Cost" ≈ "Insured Amount").  

Your goal:
- Identify all fields or equivalent expressions in the text that match the meaning of the given field list.
- Extract the most complete and precise value found for each field.
- If a field or its synonym is not found, simply skip it (do not include empty entries).
- Use contextual understanding, not only exact word matching.
- Be as detailed as possible — capture full numeric or textual values.
- If multiple candidate values exist for a field, choose the most precise and complete one.

You must return your result strictly in JSON format
Text to analyze:
'''
{text}
'''

Fields to find:
{fields_list}
"""


DATA_EXTRACT_PROMPT = """
You are an expert data extractor. Using the context below, find the value for the field: "{field_name}".
- Provide the most precise value you can find.

Context:
{context}

Return JSON
"""

PROPOSE_AND_ADD_SYNONYMS_PROMPT = """
You are a helpful assistant that finds alternative phrases (synonyms) for a given field.

Field name: "{field_name}"
Contexts (fragments from documents):
{ctx_snippets}

Task:
- Provide up to 10 short alternative phrases that can be used as synonyms for the field.
- Return JSON list of strings, e.g. ["Total Insured Value", "Declared Value"].
- Only short phrases/terms. If unsure, return an empty list.
"""