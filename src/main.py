import asyncio

from Chain import FileLoader
from Config import FILES_PATH
from Database import DatabaseClient
from Schemas import FilesExtensionEnum
from Utils import Finder, process_json_file


async def main():
    db_client = DatabaseClient()
    finder = Finder()
    try:
        await asyncio.gather(
            FileLoader.start_processor_loop(db_client),
            FileLoader.remover_loop(db_client),
            finder.start_loop(  # JSON PROCESSOR
                db_client=db_client,
                func=process_json_file,
                path=FILES_PATH,
                extension=FilesExtensionEnum.JSON,
                db_table="service"
            )
        )

    finally:
        await db_client.dispose()

if __name__ == "__main__":
    asyncio.run(main())
