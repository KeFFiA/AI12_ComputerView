import json
from pathlib import Path


from Config import llm_chat as logger
from Config.Templates import FILE_TYPE_PROMPT, PAGE_NAVIGATION_PROMPT
from Database import PDF_Queue
from Utils import extract_pdf_text

from openai import OpenAI

from Schemas import AnalysTypeEnum, FileTypeSchema, PageNavigationSchema, DefaultMessageSchema


async def main_request(client, text: str | None = None,
                       request_type: AnalysTypeEnum | None = None,
                       *,
                       path: str | Path | None = None,
                       fileid: int | None = None) -> FileTypeSchema | PageNavigationSchema | DefaultMessageSchema:
    if request_type is None:
        llm_text = text
        format = DefaultMessageSchema

    llm_client = OpenAI(base_url="http://158.255.7.14:8000/v1", api_key="not-needed")

    if request_type == AnalysTypeEnum.FILE_TYPE:
        async with client.session("service") as session:
            row: PDF_Queue = await session.get(PDF_Queue, fileid)
            text = await extract_pdf_text(client, path, fileid, pages_to_extract=[1])
            llm_text = FILE_TYPE_PROMPT.format(text=text[:1000])
            format = FileTypeSchema
            row.status_description = "Waiting for answer..."
            logger.info("Fetching File Type. Waiting for answer...")

    if request_type == AnalysTypeEnum.PAGE_NAVIGATION:
        async with client.session("service") as session:
            row = await session.get(PDF_Queue, fileid)
            text = await extract_pdf_text(client, path, fileid, pages_to_extract="2-6")
            llm_text = PAGE_NAVIGATION_PROMPT.format(text=text)
            format = PageNavigationSchema
            row.status_description = "Waiting for answer..."
            logger.info("Fetching Page Navigation exist. Waiting for answer...")


    response = llm_client.chat.completions.create(
        model="qwen2.5-72b-instruct-q8_0-00001-of-00021",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert at document type parsing.\n"
                    "Return ONLY valid JSON matching this schema:\n"
                    f"{json.dumps(format.model_json_schema(), indent=2)}"
                )
            },
            {
                "role": "user",
                "content": llm_text
            }
        ],
        temperature=0
    )

    raw = response.choices[0].message.content
    parsed = format.model_validate_json(raw)
    return parsed


if __name__ == '__main__':
    import asyncio
    from Database import DatabaseClient
    from Config import FILES_PATH
    from datetime import datetime
    path = FILES_PATH / 'Aircraft_Lease_Agreement_MSN_1487_SLX_COA_Cargo_Executed_12_20_20236765229.pdf'
    stat = path.stat()

    info = {
        "file_name": path.name,
        "size_bytes": stat.st_size,
        "created": datetime.fromtimestamp(stat.st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
    }
    print(info)
    # client = DatabaseClient()
    # test = asyncio.run(main_request(client=client, path=path, request_type=AnalysTypeEnum.PAGE_NAVIGATION))
    # print(test)
