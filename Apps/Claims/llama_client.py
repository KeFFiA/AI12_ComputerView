import os, httpx

from openai import OpenAI
from openai.types import ResponseFormatJSONSchema

LLM_API = os.environ.get("LLM_ENDPOINT", "http://212.69.84.131:8000")
main_client = OpenAI(base_url=LLM_API, api_key="llama")

async def ask_llama(prompt: str, client: OpenAI = main_client):
    response = client.chat.completions.parse(
        model="Meta-Llama-3-8B-Instruct",
        messages=[{
            "role": "system",
            "content": "You are PDF Parser expert, you must parse all possible data and create valid JSON response"
        },
            {
                "role": "user",
                "content": prompt
            }],
        temperature=0.1,
        top_p=0.95,
        response_format=ResponseFormatJSONSchema
    )

    return response.choices[0].message.content
