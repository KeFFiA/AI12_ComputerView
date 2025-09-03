import json
import re

from langchain_core.output_parsers import JsonOutputParser
from langchain_core.prompts import PromptTemplate
from langchain_core.exceptions import OutputParserException

from Database import DatabaseClient, PDF_Queue
from Config import llm, MAINEXTRACT_PROMPT
from Config import llm_log as logger
from Config.Templates import Claim


parser = JsonOutputParser(pydantic_object=Claim)

async def extract_information(fileid: int, text: str|dict, template: str = MAINEXTRACT_PROMPT):
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
                return response
            elif isinstance(response, str):
                json_match = re.search(r'\{.*\}', response, re.DOTALL)
                if json_match:
                    return json.loads(json_match.group())

            raise OutputParserException("Invalid format")

        except (OutputParserException, json.JSONDecodeError) as e:
            client = DatabaseClient()
            async with client.session("service") as session:
                row = await session.get(PDF_Queue, fileid)
                row.status_description = f"Attempt {attempt + 1} failed: {str(e)}"
                await session.commit()
            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")
            if attempt == max_retries - 1:
                raise
            continue
    return None
