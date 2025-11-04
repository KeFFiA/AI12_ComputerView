import asyncio

from Chain import FileLoader
from Database import DatabaseClient


async def main():
    db_client = DatabaseClient()
    try:
        await asyncio.gather(
            FileLoader.start_processor_loop(db_client),
            FileLoader.remover_loop(db_client)
        )
    finally:
        await db_client.dispose()

if __name__ == "__main__":
    asyncio.run(main())


