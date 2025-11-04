from pathlib import Path
from Schemas import FileTypeSchema, PageNavigationSchema
from Schemas.Enums import FileTypeEnum
from Utils import extract_pdf_text
from Config.Templates import LEASE_AGREEMENT_CONSTANTS, INSURANCE_SURVEYOR_REPORT_CONSTANTS
from Chain import main_request

async def found_number_of_pages(
        navigation_pages: str | list[int],
        file_path: str | Path,
        file_id: int
):
    """
    Find number of pages in given file, where
    """


async def processor(
        client,
        file_path: str | Path,
        file_id: int,
        file_type_response: FileTypeSchema,
        page_navigation_response: PageNavigationSchema
):
    if file_type_response.document_type == FileTypeEnum.LEASE_AGREEMENT and file_type_response.confidence > 0.8:
        fields_to_find = LEASE_AGREEMENT_CONSTANTS
    elif file_type_response.document_type == FileTypeEnum.INSURANCE_SURVEYOR_REPORT and file_type_response.confidence > 0.8:
        fields_to_find = INSURANCE_SURVEYOR_REPORT_CONSTANTS
    elif file_type_response.document_type == FileTypeEnum.PAYMENT and file_type_response.confidence > 0.8:
        ...
    else:
        ...

    if page_navigation_response.page_navigation is True and page_navigation_response.confidence > 0.8:
        document_text = await extract_pdf_text(
            client=client,
            path=file_path,
            fileid=file_id,
            pages_to_extract=page_navigation_response.pages
        )



        response = main_request(client=client, )

    else:
        document_text = await extract_pdf_text(
            client=client,
            path=file_path,
            fileid=file_id
        )

        response = main_request(client=client, )



