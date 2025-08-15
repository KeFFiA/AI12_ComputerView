import json
import re

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.exceptions import OutputParserException
from test import llm

from test.chains.templates.templates import Claim

parser = JsonOutputParser(pydantic_object=Claim)


PROMPT_TEMPLATE = "Extract all possible information from this text.\n{format_instructions}\n{text}\n\n **IMPORTANT: JSON SCHEMA**"

def extract_information(text: str|dict, template: str = PROMPT_TEMPLATE):
    prompt = PromptTemplate(
        template=template,
        input_variables=["text"],
        partial_variables={"format_instructions": parser.get_format_instructions()},
    )

    chain = prompt | llm | parser

    max_retries = 3
    for attempt in range(max_retries):
        try:
            response = chain.invoke({"text": text})

            if isinstance(response, dict):
                print(response)
                return response
            elif isinstance(response, str):
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    print(json.loads(json_match.group()))
                    return json.loads(json_match.group())

            raise OutputParserException("Invalid format")

        except (OutputParserException, json.JSONDecodeError) as e:
            print(f"Попытка {attempt + 1} не удалась: {str(e)}")
            if attempt == max_retries - 1:
                raise
            continue

    print(None)
    return None
