from pathlib import Path

from pydantic import ValidationError

from Config import PROMPT_TEMPLATE_JSON
from Config import chain as logger
from Config.Templates import Claim
from .LLMExtract import extract_information
from .LLMTools import compare_data
from Utils import extract_pdf_text, create_report
from Database import DatabaseClient, PDF_Queue
from Schemas import QueueStatusEnum


async def main_chain(client, file_path: Path, filename: str, fileid: int):
    async with client.session("service") as session:
        row = await session.get(PDF_Queue, fileid)
        try:
            row.status_description = "Stage 1. Extract text from PDF"
            row.progress_total = 6
            row.progress_done = 1
            row.progress = row.progress_done / row.progress_total * 100
            await session.commit()
            logger.info("Stage 1. Extract text from PDF")
            raw_text = await extract_pdf_text(client, file_path, fileid)

            row.status_description = "Stage 2. Extract JSON from extracted raw text. Waiting for LLM answer..."
            await session.commit()
            logger.info("Stage 2. Extract JSON from extracted raw text. Waiting for LLM answer...")
            extracted = await extract_information(client, text=raw_text, fileid=fileid)

            row.progress_done += 1
            row.progress = row.progress_done / row.progress_total * 100

            row.status_description = "Stage 3. Validate extracted JSON"
            await session.commit()
            logger.info("Stage 3. Validate extracted JSON")
            try:
                Claim(**extracted)
                row.status_description = "JSON values validated"
                row.progress_done += 1
                row.progress = row.progress_done / row.progress_total * 100
                await session.commit()
                logger.info("JSON values validated")
            except ValidationError:
                row.status_description = "Validation Error. Trying to revalidate"
                await session.commit()
                row.progress_total += 1
                row.progress = row.progress_done / row.progress_total * 100
                logger.error("Validation Error. Trying to revalidate")
                extracted = await extract_information(client, fileid=fileid, text=extracted, template=PROMPT_TEMPLATE_JSON)

            row.progress_done += 1
            row.progress = row.progress_done / row.progress_total * 100
            row.status_description = "Stage 4. Compare JSON fields with DB"
            await session.commit()
            logger.info("Stage 4. Compare JSON fields with DB")
            compared = await compare_data(extracted)

            # enriched = enrich_cause(summarized)
            # save_to_db(enriched)
            row.progress_done += 1
            row.progress = row.progress_done / row.progress_total * 100
            row.status_description = "Stage 5. Create report"
            await session.commit()
            logger.info("Stage 5. Create report")
            filename = await create_report(compared, filename)

            row.status_description = "Done"
            row.status = QueueStatusEnum.DONE.value
            row.progress = 100
            await session.commit()
            logger.info(f"Done. Created report {filename}")

            return True
        except Exception as e:
            row.status_description = str(e)
            row.status = QueueStatusEnum.FAILED.value
            await session.commit()
            logger.error(e)
            return False

    #     extracted = {
    #     "report_type": "First Advice",
    #     "msn": None,
    #     "aircraft": "Airbus A320-251N",
    #     "registration": "TF-PPF",
    #     "insured": "Fly Play",
    #     "insurer": "Starr Underwriting Agents Limited",
    #     "cause": "No. 2 engine Thrust Reverser damaged during installation",
    #     "location": "Montpellier–Méditerranée Airport, France",
    #     "dol": "2025-03-26",
    #     "indemnity_reserve": None,
    #     "indemnity_reserve_currency": None,
    #     "paid_to_date": 8000.0,
    #     "paid_to_date_currency": "GBP",
    #     "summary": "FlyPlay, Airbus A320-251N, Registration TF-PPF, No. 2 engine Thrust Reverser damaged during installation at Montpellier-Méditerranée Airport, France on 26 March 2025. The aircraft was undergoing scheduled maintenance at the Vallair facility. Following damage being sustained by Vallair to the original installed Thrust Reverser (which is being handled as a separate claim), a replacement Thrust Reverser was procured by FlyPlay and shipped to Vallair for installation. During the installation process undertaken by Vallair employees, which involved the Thrust Reverser being lifted in a sling by crane, it came into contact with the No. 6 strut installed on engine No. 2. Preliminary inspections revealed impact deformation to the inner fixed structure, outside of allowable limitations for continued operation. After undertaking detailed damage mapping, the Thrust Reverser was repaired in accordance with the Structural Repair Manual (SRM) by Vallair. McLarens Paris office was able to undertake a survey at the Vallair facility and discuss the extent of the damage sustained and repairs undertaken.",
    #     "contact_name": "Gary Clift",
    #     "contact_title": "Aviation Claims Manager",
    #     "contact_phone": "+44 (0)788 580 3530",
    #     "contact_email": "gary.clift@mclarens.com"
    # }
