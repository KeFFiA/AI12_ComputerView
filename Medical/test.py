import glob
import os
from pathlib import Path
from openai import OpenAI
from ResponseModel import InsurancesResponse

client = OpenAI(base_url="http://212.69.84.131:8000", api_key="llama")

pdf_files = sorted(glob.glob(os.path.join("/pdfs", "*.pdf")))
print(f"[INFO] Найдено {len(pdf_files)} PDF-файлов")

for pdf_path in pdf_files:
    file = client.files.create(
        file=Path(pdf_path),
        purpose="user_data"
    )

    print(file.id, file.filename)

    response = client.chat.completions.parse(
        model="Meta-Llama-3-8B-Instruct",
        messages=[
            {
                "role": "system",
                "content": "Extract all available insurance-related information from the page. The following fields should be identified and extracted if present: Company Name, Insurance Category, Number of Lives, Area of Coverage or Geographical Scope, Extended Territory for Emergency Treatment Only, Annual Aggregate Limit, Pre-existing Conditions, Network Type, OP Consultation, OP Physiotherapy, Pharmaceuticals, Diagnostics, Dental Benefit, Optical Benefit, Alternative Medicines, Maternity OP Benefit, Psychiatric OP Benefit, Outside Network Co-Insurance, IP Benefit, Maternity IP Benefit, Psychiatric IP Benefit, Organ Transplant (including donor charges but excluding cost of organ), In-patient Cash Benefit (if free treatment taken at a government facility in UAE), Annual Health Check-up, Value-Added Services, Gross Premium (including VAT & Basmah), Cost Per Member"
            },
            {
                "role": "user",
                "content": file.id
            }
        ],
        response_format=InsurancesResponse
    )

    print(response.choices[0].message.content)

# from pydantic import BaseModel
#
# from pydantic_ai import Agent
# from pydantic_ai.models.openai import OpenAIModel
# from pydantic_ai.providers.openai import OpenAIProvider
#
# ollama_model = OpenAIModel(
#     model_name='qwen2.5-coder:7b',
#     provider=OpenAIProvider(base_url='http://192.168.1.74:11434/v1'),
# )
#
#
# class CityLocation(BaseModel):
#     city: str
#     country: str
#
#
# agent = Agent(model=ollama_model, output_type=CityLocation)
#
# result = agent.run_sync('Where were the olympics held in 2012?')
# print(result.output)

