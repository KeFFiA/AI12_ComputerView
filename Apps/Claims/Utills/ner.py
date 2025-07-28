from transformers import pipeline

ner_pipeline = pipeline("token-classification", model="dslim/bert-base-NER", aggregation_strategy="simple", device="cuda")

def extract_entities(text: str) -> dict:
    raw_entities = ner_pipeline(text)
    result = {"ORG": [], "LOC": [], "DATE": [], "MONEY": [], "PER": []}

    for ent in raw_entities:
        label = ent["entity_group"]
        if label in result:
            result[label].append(ent["word"])

    # Удаление дубликатов
    return {k: list(set(v)) for k, v in result.items()}