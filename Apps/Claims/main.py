import asyncio

from Chain import FileLoader

if __name__ == "__main__":
    asyncio.run(FileLoader.start_processor_loop())


