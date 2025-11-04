from pathlib import Path
from typing import Dict

from Config import chain as logger
from Schemas import FieldExtractionResult
from Schemas.Enums import FileTypeEnum
from Utils import get_constants_by_filetype, find_field_value_via_embeddings


async def processor_with_embeddings(
        file_path: Path,
        file_type: FileTypeEnum = FileTypeEnum.NOT_DEFINED,
):
    """
    Processes a document:
    1) Extracts text (all or by page)
    2) Updates local and global embeddings
    3) Searches for values of all fields using local embeddings + LLM
    4) Returns a dictionary with the results
    """
    results: Dict[str, FieldExtractionResult] = {}
    try:
        fields_to_find = get_constants_by_filetype(file_type)

        for field in fields_to_find:
            extracted = await find_field_value_via_embeddings(
                file_name=file_path.name,
                field_name=field,
                top_k_per_term=3
            )
            results[field] = extracted

        print(results)
        return results
    except Exception as e:
        logger.exception(f"Error in processor_with_embeddings: {e}", exc_info=True)
        return {}


__all__ = ["processor_with_embeddings"]