from transformers import pipeline

event_pipeline = pipeline("zero-shot-classification", model="facebook/bart-large-mnli")

# Возможные типы событий
EVENT_LABELS = [
    "engine surge",
    "bird strike",
    "collision",
    "fire",
    "insurance claim",
    "component failure",
    "technical damage",
    "accident",
    "repair",
    "inspection"
]

def extract_events(text: str) -> list:
    result = event_pipeline(text, candidate_labels=EVENT_LABELS, multi_label=True)
    threshold = 0.5
    return [label for label, score in zip(result["labels"], result["scores"]) if score > threshold]
