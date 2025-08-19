import glob
import os
import shutil
from pathlib import Path
from time import sleep

from Config.Logger import setup_logger

from chain import process_pdf

logger = setup_logger(__name__)

PATH = Path(os.getenv("LISTEN_DIR", "data/input_pdfs"))
NOPASSED_DIR = Path(os.getenv("LISTEN_DIR", "data/nopassed_pdfs"))

PATH.mkdir(parents=True, exist_ok=True)
NOPASSED_DIR.mkdir(parents=True, exist_ok=True)

def findfiles():
    while True:
        pdf_files = sorted(glob.glob(os.path.join(PATH, "*.pdf")))
        if len(pdf_files) > 0:
            logger.info(f"{len(pdf_files)} PDF found")
            for pdf_file in pdf_files:
                filename = os.path.splitext(os.path.basename(pdf_file))[0]
                logger.info(f"Processing file: {filename}")

                result = process_pdf(pdf_file)
                if result:
                    os.remove(pdf_file)
                else:
                    target_path = NOPASSED_DIR / os.path.basename(pdf_file)
                    shutil.move(pdf_file, target_path)
                    logger.info(f"Moved {pdf_file} -> {target_path}")

        sleep(60)

