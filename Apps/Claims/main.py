import asyncio
import glob
import os

from Utills.normalizer import normalize_answer
from parser import get_pdf_text
from chunker import split_text
from llama_client import ask_llama
from Utills.aggregator import aggregate_normalized


INPUT_DIR = "data/input_pdfs_claims"


async def main(path):
    print('Start processing...')
    try:
        print('Extracting text...')
        text = get_pdf_text(path=path)
        if not text:
            print({"error": "No text found in PDF"})
        print("Text extracted")

        print("Splitting text to chunks")
        chunks = list(split_text(text))
        results = []

        for i, chunk in enumerate(chunks):
            prompt = f"Here is part of the document:\n{chunk}\n\nCheck and create JSON"
            print("Sending chunk {}...".format(i))
            answer = await ask_llama(prompt)
            print("Got answer\nNormalizing...")
            structured = normalize_answer(answer)

            results.append({
                "chunk_id": i,
                "raw_text": chunk,
                "llm_answer": answer.strip(),
                "normalized": structured
            })
        print("Aggregating results...")
        aggregated = aggregate_normalized(results)
        print("Saving results...")


        print({
            "total_chunks": len(chunks),
            "results": results,
            "aggregated_summary": aggregated
        })

        print('\n\n\n______________________\n\n\n', aggregated)
    except Exception as e:
        print({"error": e})


async def process_all_pdfs():
    print("[INFO] Загрузка шаблона Excel...")

    pdf_files = sorted(glob.glob(os.path.join(INPUT_DIR, "*.pdf")))
    print(f"[INFO] Найдено {len(pdf_files)} PDF-файлов")

    for pdf_path in pdf_files:
        company_name = os.path.splitext(os.path.basename(pdf_path))[0]
        print(f"\n[INFO] Обработка файла: {company_name}")
        await main(path=pdf_path)


if __name__ == '__main__':
    asyncio.run(process_all_pdfs())


# app = FastAPI()

# @app.post("/process/")
# async def process_pdf(file: UploadFile = File(...)):
#     suffix = os.path.splitext(file.filename)[-1]
#     if suffix.lower() != ".pdf":
#         return {"error": "Only PDF supported"}
#
#     with NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
#         shutil.copyfileobj(file.file, tmp)
#         tmp_path = tmp.name
#
#     try:
#         text = get_pdf_text(tmp_path)
#         if not text:
#             return {"error": "No text found in PDF"}
#
#         chunks = list(split_text(text))
#         responses = []
#
#         for i, chunk in enumerate(chunks):
#             prompt = f"Вот часть документа:\n{chunk}\n\nВыдели ключевые факты, даты, суммы, номера, названия и роли сторон."
#             answer = await ask_llama(prompt)
#             responses.append({
#                 "chunk_id": i,
#                 "text": chunk,
#                 "answer": answer.strip()
#             })
#
#         return {
#             "total_chunks": len(chunks),
#             "results": responses
#         }
#     finally:
#         os.remove(tmp_path)
