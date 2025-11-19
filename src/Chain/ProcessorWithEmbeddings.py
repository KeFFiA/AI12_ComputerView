from pathlib import Path

from Config import chain as logger
from Database import PDF_Queue
from Schemas.Enums import FileTypeEnum
from Utils import get_constants_by_filetype, find_field_value_via_embeddings


async def processor_with_embeddings(
        client,
        file_id: int,
        file_path: Path,
        file_type: FileTypeEnum = FileTypeEnum.NOT_DEFINED,

):
    """
    Processes a document:
    1) Extracts text (all or by page)
    2) Updates local and global embeddings
    3) Searches for values of all fields using local embeddings + LLM
    4) Returns a list with the results
    """
    results: list = []
    try:
        async with client.session("service") as session:
            row: PDF_Queue = await session.get(PDF_Queue, file_id)
            fields_to_find = get_constants_by_filetype(file_type)
            row.progress_total += len(fields_to_find)
            if isinstance(fields_to_find, dict):
                for field, field_value in fields_to_find.items():
                    row.status_description = "Parsing field: {}...".format(field)
                    extracted = await find_field_value_via_embeddings(
                        file_name=file_path.name,
                        field_name=field,
                        field_additional_info=field_value,
                        top_k_per_term=3
                    )
                results.append(extracted)
                row.progress_done += 1
                row.progress = row.progress_done / row.progress_total * 100
                await session.commit()
        return results
    except Exception as e:
        async with client.session("service") as session:
            row: PDF_Queue = await session.get(PDF_Queue, file_id)
            row.status_description = f"Error while parse field '{field}': {e}"
            await session.commit()
        logger.exception(f"Error while parse field '{field}': {e}", exc_info=True)
        return {}


__all__ = ["processor_with_embeddings"]