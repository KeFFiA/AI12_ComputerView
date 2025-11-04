from enum import Enum


class QueueStatusEnum(str, Enum):
    QUEUED = "Queued"
    PROCESSING = "Processing"
    DONE = "Done"
    FAILED = "Failed"


class AnalysTypeEnum(str, Enum):
    FILE_TYPE = "File type"
    PAGE_NAVIGATION = "Page navigation"
    NOT_DEFINED = "Not defined"


class FileTypeEnum(str, Enum):
    LEASE_AGREEMENT = "Lease agreement"
    PAYMENT = "Payment document"
    INSURANCE_SURVEYOR_REPORT = "Insurance Surveyor Report"
    NOT_DEFINED = "Not defined"


__all__ = [
    "QueueStatusEnum", "AnalysTypeEnum", "FileTypeEnum"
]
