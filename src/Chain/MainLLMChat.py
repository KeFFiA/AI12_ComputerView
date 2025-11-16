from pathlib import Path


from Config import OllamaClient
from Config import llm_chat as logger
from Config.Templates import FILE_TYPE_PROMPT, PAGE_NAVIGATION_PROMPT
from Database import PDF_Queue
from Utils import extract_pdf_text

from Schemas import AnalysTypeEnum, FileTypeSchema, PageNavigationSchema, DefaultMessageSchema


async def main_request(client, text: str | None = None,
                       request_type: AnalysTypeEnum | None = None,
                       *,
                       path: str | Path | None = None,
                       fileid: int | None = None) -> FileTypeSchema | PageNavigationSchema | DefaultMessageSchema:
    llm_client = await OllamaClient().AsyncClient
    if request_type is None:
        llm_text = text
        format = DefaultMessageSchema
    if request_type == AnalysTypeEnum.FILE_TYPE:
        async with client.session("service") as session:
            row: PDF_Queue = await session.get(PDF_Queue, fileid)
            text = await extract_pdf_text(client, path, fileid, pages_to_extract=[1])
            llm_text = FILE_TYPE_PROMPT.format(text=text[:3000])
            format = FileTypeSchema
            row.status_description = "Waiting for answer..."
    if request_type == AnalysTypeEnum.PAGE_NAVIGATION:
        async with client.session("service") as session:
            row = await session.get(PDF_Queue, fileid)
            text = await extract_pdf_text(client, path, fileid, pages_to_extract="2-6")
            llm_text = PAGE_NAVIGATION_PROMPT.format(text=text)
            format = PageNavigationSchema
            row.status_description = "Waiting for answer..."


    response = await llm_client.chat(messages=[{
        'role': 'user',
        'content': llm_text
    }], format=format.model_json_schema(), think=True)
    try:
        return format.model_validate_json(response.message.content)
    except:
        try:
            return format.model_validate_json(response.message.content.removeprefix('{"'))
        except:
            return format.model_validate_json(response.message.content.removeprefix('{'))


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
