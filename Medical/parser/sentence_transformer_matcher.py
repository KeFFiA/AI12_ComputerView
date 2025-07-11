from sentence_transformers import SentenceTransformer, util
import torch

# Загружаем модель один раз
_model = SentenceTransformer("all-MiniLM-L6-v2")

def match_with_embeddings(query, lines):
    """
    Использует эмбеддинги для поиска наиболее близкой строки по смыслу.
    Возвращает строку и оценку схожести (от 0 до 1).
    """
    if not lines:
        return None, 0.0

    query_emb = _model.encode(query, convert_to_tensor=True)
    lines_emb = _model.encode(lines, convert_to_tensor=True)

    cosine_scores = util.cos_sim(query_emb, lines_emb)[0]  # shape: [len(lines)]
    best_score, best_idx = torch.max(cosine_scores, dim=0)

    return lines[best_idx], float(best_score)