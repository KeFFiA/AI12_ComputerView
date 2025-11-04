from pathlib import Path
from typing import Sequence, Union

from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfReader

from Config import pdf_extractor as logger
from Database import PDF_Queue


def parse_page_ranges(pages: Union[str, Sequence[int], None], total_pages: int) -> list[int]:
    """
    Convert a page selection (string like "1-3,5,7-9" or list[int])
    into a validated sorted list of unique page numbers.
    """
    if not pages:
        return list(range(1, total_pages + 1))

    if isinstance(pages, str):
        result = set()
        for part in pages.split(','):
            part = part.strip()
            if '-' in part:
                start, end = part.split('-', 1)
                try:
                    start, end = int(start), int(end)
                    result.update(range(start, end + 1))
                except ValueError:
                    continue
            else:
                try:
                    result.add(int(part))
                except ValueError:
                    continue
        pages = sorted(result)
    else:
        # sequence of ints
        pages = sorted({int(p) for p in pages})

    return [p for p in pages if 1 <= p <= total_pages]


def get_number_of_pages(path: Path) -> int:
    reader = PdfReader(path)
    total_pages = len(reader.pages)
    return total_pages


async def extract_pdf_text(
    client,
    path: str | Path,
    fileid: int,
    pages_to_extract: Union[str, Sequence[int], None] = None
) -> str:
    """
    Extract text from specific PDF pages (or all if not specified).
    Falls back to OCR if no text is found.

    :param client: async DB client
    :param path: Path to the PDF
    :param fileid: ID in PDF_Queue table
    :param pages_to_extract: list[int] or string like "1-3,5,7-9"
    :return: Extracted text as string
    """
    async with client.session("service") as session:
        row = await session.get(PDF_Queue, fileid)
        if not row:
            logger.error(f"Row with id={fileid} not found in DB")
            # return ""

        try:
            logger.info("Trying to extract PDF text...")
            # row.status_description = "Trying to extract PDF text"
            # await session.commit()

            reader = PdfReader(path)
            total_pages = len(reader.pages)

            pages = parse_page_ranges(pages_to_extract, total_pages)

            text = ''.join(
                reader.pages[p - 1].extract_text() or ''
                for p in pages
            )

            if len(text.strip()) > 50:
                logger.info(f"Text extraction completed. Extracted {len(pages)} pages.")
                # row.progress_done += len(pages)
                # row.progress = row.progress_done / row.progress_total * 100
                # row.status_description = f"Extraction completed. Extracted {len(pages)} pages"
                # await session.commit()
                return text

            raise ValueError("No text extracted from PDF, switching to OCR")

        except Exception as e:
            logger.warning(f"Text extraction failed ({e}), switching to OCR...")
            text_parts = []

            pages = parse_page_ranges(pages_to_extract, len(PdfReader(path).pages))

            images = []
            for p in pages:
                imgs = convert_from_path(path, dpi=200, first_page=p, last_page=p)
                images.extend(imgs)

            total_pages = len(images)
            row.progress_total += total_pages
            row.status_description = "Using OCR..."
            await session.commit()

            for i, img in enumerate(images, start=1):
                page_text = pytesseract.image_to_string(img)
                text_parts.append(page_text)

                row.progress_done += 1
                row.progress = row.progress_done / row.progress_total * 100
                row.status_description = f"OCR in progress: page {i}/{total_pages}"
                await session.commit()

            final_text = ''.join(text_parts)

            row.status_description = f"OCR extraction completed. {total_pages} pages processed."
            row.progress_done += 1
            row.progress = row.progress_done / row.progress_total * 100
            await session.commit()

            return final_text
