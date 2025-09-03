from pdf2image import convert_from_path
import pytesseract
from PyPDF2 import PdfReader

from Config import pdf_extractor as logger
from Database import DatabaseClient, PDF_Queue

from Schemas import QueueStatusEnum


async def extract_pdf_text(path: str, fileid: int) -> str:
    client = DatabaseClient()
    async with client.session("service") as session:
        row = await session.get(PDF_Queue, fileid)
        if not row:
            logger.error(f"Row with id={fileid} not found in DB")
            return ""

        try:
            logger.info("Trying to extract PDF text...")
            row.status_description = "Trying to extract PDF text"
            await session.commit()

            reader = PdfReader(path)
            text = ''.join(page.extract_text() or '' for page in reader.pages)

            if len(text.strip()) > 50:
                logger.info(f"Extraction completed. Extracted {len(reader.pages)} pages")
                row.status_description = f"Extraction completed. Extracted {len(reader.pages)} pages"
                await session.commit()
                return text

            raise ValueError("No text extracted from PDF, switching to OCR")

        except Exception:
            logger.exception("Extract PDF text failed")
            row.status_description = "Extract PDF text failed. Switching to OCR..."
            row.status = QueueStatusEnum.FAILED.value
            await session.commit()

        # OCR fallback
        logger.info("Using OCR...")
        row.status_description = "Using OCR..."
        await session.commit()

        images = convert_from_path(path, dpi=200)
        total_pages = len(images)
        text_parts = []

        for i, img in enumerate(images, start=1):
            page_text = pytesseract.image_to_string(img)
            text_parts.append(page_text)

            row.status_description = f"OCR in progress: page {i}/{total_pages}"
            await session.commit()
            logger.info(f"OCR page {i}/{total_pages}")

        final_text = ''.join(text_parts)

        row.status_description = f"OCR extraction completed. {total_pages} pages processed."
        await session.commit()

        return final_text


