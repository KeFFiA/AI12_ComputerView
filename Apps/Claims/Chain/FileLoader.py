import asyncio
import os
import shutil
from pathlib import Path

from Config import FILES_PATH, NOPASSED_PATH
from Config import file_processor as logger

from .ProcessPDF import main_chain

from Database import DatabaseClient, PDF_Queue
from Schemas import QueueStatusEnum
from sqlalchemy import select


async def start_processor_loop():
    client = DatabaseClient()
    while True:
        async with client.session("service") as session:
            result = await session.execute(
                select(PDF_Queue)
                .where(PDF_Queue.status == "Queued")
                .order_by(PDF_Queue.queue_position.asc())
                .limit(2)
            )
            rows = result.scalars().all()

            if rows:
                for row in rows:
                    path: Path = FILES_PATH / row.filename
                    row.status = QueueStatusEnum.PROCESSING.value
                    await session.commit()
                    logger.info(f"Processing file: {row.filename}")
                    process_result = await main_chain(path, row.filename, row.id)
                    if process_result:
                        row.status = QueueStatusEnum.DONE.value
                        await session.commit()
                        os.remove(path)
                        logger.debug(f"Removed {row.filename}")
                    else:
                        row.status = QueueStatusEnum.FAILED.value
                        await session.commit()
                        target_path = NOPASSED_PATH / row.filename
                        shutil.move(path, target_path)
                        logger.info(f"Moved {row.filename} -> {NOPASSED_PATH}")

        logger.debug("Waiting for new files")
        await asyncio.sleep(5)
