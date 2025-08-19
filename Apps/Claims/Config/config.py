import os

import langchain_ollama
from dotenv import load_dotenv

load_dotenv()

DB_URI_MAIN=os.getenv("DB_URI_MAIN")

llm = langchain_ollama.OllamaLLM(
    # model="deepseek-r1:8b-0528-qwen3-q4_K_M",
    # model="llama3.1:8b-instruct-q8_0",
    model="qwen2.5:32b-instruct-q4_0",
    base_url="http://212.69.84.131:11434",
    temperature=0.0
)


