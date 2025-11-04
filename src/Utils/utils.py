from Schemas.Enums import FileTypeEnum


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



