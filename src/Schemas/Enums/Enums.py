from enum import Enum as __enum


class QueueStatusEnum(str, __enum):
    QUEUED = "Queued"
    PROCESSING = "Processing"
    DONE = "Done"
    FAILED = "Failed"


class AnalysTypeEnum(str, __enum):
    FILE_TYPE = "File type"
    PAGE_NAVIGATION = "Page navigation"
    NOT_DEFINED = "Not defined"


class FileTypeEnum(str, __enum):
    LEASE_AGREEMENT = "Lease agreement"
    PAYMENT = "Payment document"
    INSURANCE_SURVEYOR_REPORT = "Insurance Surveyor Report"
    NOT_DEFINED = "Not defined"


class FilesExtensionEnum(str, __enum):
    CSV = "csv"
    JSON = "json"
    EXCEL = "xlsx"
    TXT = "txt"


__all__ = [
    "QueueStatusEnum", "AnalysTypeEnum", "FileTypeEnum", "FilesExtensionEnum"
]
