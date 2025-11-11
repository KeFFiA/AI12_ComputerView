from datetime import datetime
from pathlib import Path

from pydantic import ValidationError

from Config import chain as logger
from .MainLLMChat import main_request
from .ProcessorWithEmbeddings import processor_with_embeddings
from Utils import create_report, process_document, get_number_of_pages, dump_to_json
from Database import PDF_Queue, DatabaseClient
from Schemas import QueueStatusEnum, AnalysTypeEnum, DocumentMetadata
from Schemas.Enums import FileTypeEnum


async def main_chain(client, file_path: Path, filename: str, fileid: int):
    try:
        async with client.session("service") as session:
            row: PDF_Queue = await session.get(PDF_Queue, fileid)
            logger.info("Stage 1. Analysing file type")
            row.status_description = "Stage 1. Analysing file type"
            row.progress_total = 8
            row.progress_done = 1
            row.progress = row.progress_done / row.progress_total * 100
            await session.commit()
            file_type_response = await main_request(client=client, path=file_path, fileid=fileid, request_type=AnalysTypeEnum.FILE_TYPE)
            row.status_description = f"File type: {file_type_response.document_type.value}"
            logger.debug(f"File type: {file_type_response.document_type.value}")

        async with client.session("service") as session:
            row: PDF_Queue = await session.get(PDF_Queue, fileid)
            logger.info("Stage 2. Creating embeddings")
            row.status_description = "Stage 2. Creating embeddings"
            row.progress_done += 1
            row.progress = row.progress_done / row.progress_total * 100
            await session.commit()
            metadata = DocumentMetadata(file_name=file_path.name,
                                        created=datetime.fromtimestamp(file_path.stat().st_ctime).strftime('%Y-%m-%d %H:%M:%S'),
                                        pages=get_number_of_pages(path=file_path),
                                        size=file_path.stat().st_size,
                                        file_type=file_type_response.document_type
                                        if file_type_response.confidence > 0.8
                                        else FileTypeEnum.NOT_DEFINED)
            _result, _desc = await process_document(client=client, file_path=file_path, file_id=fileid, metadata=metadata.model_dump())
            if not _result:
                logger.debug("Embeddings hadn't created. \n{}".format(_desc))
                row.status_description = "Embeddings hadn't created. \n{}".format(_desc)


        async with client.session("service") as session:
            row: PDF_Queue = await session.get(PDF_Queue, fileid)
            logger.info("Stage 3. Fetching data")
            row.status_description = "Stage 3. Fetching data"
            row.progress_done += 1
            row.progress = row.progress_done / row.progress_total * 100
            await session.commit()
            response = await processor_with_embeddings(client=client, file_id=fileid,
                                                       file_path=file_path, file_type=file_type_response.document_type)

        async with client.session("service") as session:
            row = await session.get(PDF_Queue, fileid)
            row.progress_done += 1
            row.progress = row.progress_done / row.progress_total * 100
            row.status_description = "Stage 4. Normalize fetched data"
            await session.commit()
            logger.info("Stage 4. Normalize fetched data")
            compared = await dump_to_json(response)


        async with client.session("service") as session:
            row = await session.get(PDF_Queue, fileid)
            row.progress_done += 1
            row.progress = row.progress_done / row.progress_total * 100
            row.status_description = "Stage 5. Create report"
            await session.commit()
            logger.info("Stage 5. Create report")
            filename = await create_report(client, compared, filename)

        async with client.session("service") as session:
            row = await session.get(PDF_Queue, fileid)
            row.status_description = "Done"
            row.status = QueueStatusEnum.DONE.value
            row.progress = 100
            await session.commit()
            logger.info(f"Done. Created report {filename}")

        return True
    except Exception as e:
        async with client.session("service") as session:
            row = await session.get(PDF_Queue, fileid)
            row.status_description = str(e)
            row.status = QueueStatusEnum.FAILED.value
            await session.commit()
        logger.error(e)
        return False


if __name__ == "__main__":
    import asyncio
    from Config import FILES_PATH
    client = DatabaseClient()
    file_path = FILES_PATH / 'Aircraft_Lease_Agreement_MSN_1487_SLX_COA_Cargo_Executed_12_20_20236765229.pdf'
    asyncio.run(main_chain(client=client, file_path=file_path, filename=file_path.name, fileid=1))

