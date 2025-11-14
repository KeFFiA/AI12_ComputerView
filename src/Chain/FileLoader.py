import asyncio
import os
import shutil
from pathlib import Path

from Config import FILES_PATH, NOPASSED_PATH
from Config import file_processor as logger
from Utils import remove_from_queue

from .Pipeline import main_chain

from Database import PDF_Queue
from Schemas import QueueStatusEnum
from sqlalchemy import select


async def start_processor_loop(client):
    logger.info("Starting main loop")
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
                    logger.info("Test in loop 1, file: {}".format(path))
                    row.status = QueueStatusEnum.PROCESSING.value
                    await session.commit()
                    logger.info(f"Processing file: {row.filename}")
                    process_result = await main_chain(client, path, row.filename, row.id)
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


async def remover_loop(client):
    logger.info("Starting remover loop")
    while True:
        async with client.session("service") as session:
            result = await remove_from_queue(session)
            if result != 0:
                logger.info(f"Removed {result} records")
        await asyncio.sleep(10800)


