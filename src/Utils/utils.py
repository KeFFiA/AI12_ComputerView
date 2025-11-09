from Schemas.Enums import FileTypeEnum
from pydantic import ValidationError


def get_constants_by_filetype(file_type: FileTypeEnum = FileTypeEnum.NOT_DEFINED) -> list | str | int | None:
    from Config.Templates import INSURANCE_SURVEYOR_REPORT_CONSTANTS, LEASE_AGREEMENT_CONSTANTS
    if file_type == FileTypeEnum.LEASE_AGREEMENT:
        return LEASE_AGREEMENT_CONSTANTS
    elif file_type == FileTypeEnum.INSURANCE_SURVEYOR_REPORT:
        return INSURANCE_SURVEYOR_REPORT_CONSTANTS
    elif file_type == FileTypeEnum.PAYMENT:
        ... # TODO: Create Payment constants
    else:
        return None


def match_schema(data: dict, *schemas):
    matches = []
    for schema in schemas:
        try:
            schema.model_validate(data)
            matches.append(schema)
        except ValidationError:
            pass
    return matches

__all__ = [
    "get_constants_by_filetype", "match_schema"
]

