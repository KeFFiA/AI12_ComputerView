import json
from pathlib import Path
from typing import List, Optional, Tuple, Dict

import numpy as np
from pgvector import Vector
from sqlalchemy import select, func

from Config import OllamaClient, EMBED_MODEL, LLM_MODEL, EMBED_BATCH, DATA_EXTRACT_PROMPT, \
    PROPOSE_AND_ADD_SYNONYMS_PROMPT
from Database import DatabaseClient
from Database.Models import DocumentEmbedding, GlobalEmbedding, FieldSynonym
from Schemas import FieldExtractionResult
from Utils import extract_pdf_text

GLOBAL_MODEL = LLM_MODEL
LOCAL_MODEL = EMBED_MODEL


def chunk_text(text: str, max_words: int = 200, overlap: int = 30) -> List[str]:
    words = text.split()
    chunks = []
    i = 0
    while i < len(words):
        chunk_words = words[i: i + max_words]
        chunks.append(" ".join(chunk_words))
        i += max_words - overlap
    return chunks


def cosine_similarity(a: np.ndarray, b: np.ndarray) -> float:
    if np.linalg.norm(a) == 0 or np.linalg.norm(b) == 0:
        return 0.0
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


async def get_embeddings(texts: List[str], model) -> List[List[float]]:
    out_vectors: List[List[float]] = []
    llm_client = await OllamaClient(model).AsyncClient

    for i in range(0, len(texts), EMBED_BATCH):
        batch = texts[i: i + EMBED_BATCH]
        resp = await llm_client.embeddings(input=batch)

        for item in resp.embeddings:
            if isinstance(item, (list, tuple)):
                out_vectors.append([float(x) for x in item])
            else:
                out_vectors.append([])

    while len(out_vectors) < len(texts):
        out_vectors.append([])

    return out_vectors


async def upsert_document_embeddings(
        file_name: str, full_text: str, metadata: Optional[dict] = None
):
    client = DatabaseClient()
    chunks = chunk_text(full_text)
    if not chunks:
        return 0

    embeddings = await get_embeddings(chunks, model=LOCAL_MODEL)

    async with client.session("service") as session:
        for idx, (txt, emb) in enumerate(zip(chunks, embeddings)):
            if not emb:
                continue

            embedding_list = [float(x) for x in emb]

            row = DocumentEmbedding(
                file_name=file_name,
                chunk_index=idx,
                text=txt,
                embedding=Vector(embedding_list),
                meta_data=json.dumps(metadata) if metadata else None
            )
            session.add(row)
        await session.commit()
        # Return number of chunks attempted (or stored) — choose stored count next
        async with client.session("service") as session:
            q = await session.execute(
                select(func.count()).select_from(DocumentEmbedding).where(DocumentEmbedding.file_name == file_name))
            cnt = q.scalar_one_or_none() or 0
        return cnt


async def upsert_global_embeddings(full_text: str, metadata: Optional[dict] = None):
    client = DatabaseClient()
    chunks = chunk_text(full_text)
    if not chunks:
        return 0

    embeddings = await get_embeddings(chunks, model=LOCAL_MODEL)

    async with client.session("service") as session:
        for idx, (txt, emb) in enumerate(zip(chunks, embeddings)):
            emb_clean = np.array([float(x) for x in emb], dtype=np.float32)
            if emb_clean.size == 0:
                continue
            row = GlobalEmbedding(
                text=txt,
                embedding=Vector(emb_clean.tolist()),
                meta_data=json.dumps(metadata) if metadata else None
            )
            session.add(row)
        await session.commit()

        # return count
        async with client.session("service") as session:
            q = await session.execute(select(func.count()).select_from(GlobalEmbedding))
            cnt = q.scalar_one_or_none() or 0
            return cnt


async def semantic_search_local(query: str, file_name: str, top_k: int = 10) -> List[Tuple[float, DocumentEmbedding]]:
    """
    Semantic search by local embeddings.
    """
    client = DatabaseClient()

    q_embs = await get_embeddings([query], model=LOCAL_MODEL)
    if not q_embs or not isinstance(q_embs[0], (list, tuple)) or len(q_embs[0]) == 0:
        return []

    q_emb = Vector(q_embs[0])

    stmt = (
        select(
            DocumentEmbedding,
            DocumentEmbedding.embedding.cosine_distance(q_emb).label("dist")
        )
        .where(DocumentEmbedding.file_name == file_name)
        .order_by("dist")
        .limit(top_k)
    )

    async with client.session("service") as session:
        res = await session.execute(stmt)
        rows = res.all()

        results: List[Tuple[float, DocumentEmbedding]] = []
        for row in rows:
            if hasattr(row, "_mapping"):
                doc = row._mapping[DocumentEmbedding]
                dist = row._mapping["dist"]

                sim = 1.0 / (1.0 + float(dist)) if dist is not None else 0.0
                results.append((sim, doc))

        return results


async def semantic_search_global(
        query: str,
        top_k: int = 5
) -> list[tuple[float, "GlobalEmbedding"]]:
    """
    Semantic search by global embeddings (corpus of all documents)
    """
    client = DatabaseClient()

    q_embs = await get_embeddings([query], model=LOCAL_MODEL)
    if not q_embs or not isinstance(q_embs[0], (list, tuple)) or len(q_embs[0]) == 0:
        # logger.warning(f"Empty embedding for query '{query}' — returning []")
        return []
    q_emb = np.array(q_embs[0], dtype=np.float32)

    stmt = (
        select(GlobalEmbedding, (GlobalEmbedding.embedding.op("<->")(q_emb)).label("dist"))
        .order_by("dist")
        .limit(top_k)
    )

    async with client.session("service") as session:
        res = await session.execute(stmt)
        rows = res.all()
        results: List[Tuple[float, GlobalEmbedding]] = []
        for row in rows:
            try:
                mapping = row._mapping
                dist = mapping.get("dist", None)
                doc = mapping.get(GlobalEmbedding.__name__.lower()) or mapping.get(0) or mapping.get(GlobalEmbedding)
            except Exception:
                try:
                    doc = row[0]
                    dist = row[1]
                except Exception:
                    # logger.warning("Unexpected row shape from semantic_search_global; skipping row.")
                    continue

            try:
                sim = 1.0 / (1.0 + float(dist)) if dist is not None else 0.0
            except Exception:
                sim = 0.0

            if not hasattr(doc, "text"):
                #                 logger.warning("Row returned by global search not ORM object; skipping.")
                continue

            results.append((sim, doc))
        return results


async def seed_synonyms(seeds: Dict[str, List[str]]):
    """
    Loads pre-defined synonyms into the FieldSynonym table.
    seeds: {"Agreed Value": ["Declared Value", "Total Insured Value"], ...}
    """
    client = DatabaseClient()

    async with client.session("service") as session:
        for field, syns in seeds.items():
            for s in syns:
                # check exists
                q = await session.execute(
                    select(FieldSynonym).where(FieldSynonym.field_name == field).where(FieldSynonym.synonym == s))
                if q.scalars().first():
                    continue
                fs = FieldSynonym(field_name=field, synonym=s, created_source="seed")
                session.add(fs)
        await session.commit()


async def ensure_synonym_embeddings():
    """
    Iterates through all FieldSynonym records without embedding and calculates the synonym embeddings, storing them in a table (cache).
    """
    client = DatabaseClient()

    async with client.session("service") as session:
        q = await session.execute(select(FieldSynonym).where(FieldSynonym.embedding == None))
        rows = q.scalars().all()
        texts = [r.synonym for r in rows]
        if not texts:
            return
        embeddings = await get_embeddings(texts, model=LOCAL_MODEL)
        for r, emb in zip(rows, embeddings):
            emb_clean = np.array([float(x) for x in emb], dtype=np.float32)
            r.embedding = emb_clean.tolist()
            r.created_source = r.created_source or "auto_cached"
        await session.commit()


async def propose_and_add_synonyms(
        field_name: str,
        contexts: List[str],
        min_confidence: float = 0.6
) -> List[str]:
    """
    Asks LLM to suggest synonyms for a field based on contexts.
    Stores them in the FieldSynonym table.
    """
    client = DatabaseClient()
    llm_client = await OllamaClient(LLM_MODEL).AsyncClient

    ctx_snippets = "\n\n---\n\n".join(contexts[:6])  # максимум 6 фрагментов
    prompt = PROPOSE_AND_ADD_SYNONYMS_PROMPT.format(ctx_snippets=ctx_snippets, field_name=field_name)
    chat_resp = await llm_client.chat(
        messages=[{"role": "user", "content": prompt}],
        keep_alive=True
    )

    content = chat_resp.message.content
    added: List[str] = []

    try:
        start = content.find("[")
        end = content.rfind("]") + 1
        if start != -1 and end != -1:
            jstr = content[start:end]
            candidates = json.loads(jstr)
            if isinstance(candidates, list):
                async with client.session("service") as session:
                    for cand in candidates:
                        cand_s = cand.strip()
                        if not cand_s:
                            continue
                        q = await session.execute(
                            select(FieldSynonym).where(
                                FieldSynonym.field_name == field_name,
                                FieldSynonym.synonym == cand_s
                            )
                        )
                        if q.scalars().first():
                            continue
                        fs = FieldSynonym(field_name=field_name, synonym=cand_s, created_source="auto")
                        session.add(fs)
                        added.append(cand_s)
                    await session.commit()
    except Exception:
        pass

    if added:
        await ensure_synonym_embeddings()

    return added


async def find_field_value_via_embeddings(
        file_name: str,
        field_name: str,
        top_k_per_term: int = 3
) -> FieldExtractionResult:
    """
    1) Loads synonyms for the field
    2) Runs semantic_search_local on all terms
    3) Deduplicates the results and generates context
    4) Sends the context to LLM to extract value, confidence, and reason
    5) Asks LLM to suggest new synonyms and saves them
    """
    client = DatabaseClient()
    llm_client = await OllamaClient(LLM_MODEL).AsyncClient

    async with client.session("service") as session:
        q = await session.execute(select(FieldSynonym).where(FieldSynonym.field_name == field_name))
        synonyms_rows = q.scalars().all()
        synonyms = [r.synonym for r in synonyms_rows]

    search_terms = [field_name] + synonyms

    gathered_matches: List[tuple[float, DocumentEmbedding]] = []
    for term in search_terms:
        results = await semantic_search_local(term, file_name=file_name, top_k=top_k_per_term)
        gathered_matches.extend(results)

    gathered_matches.sort(key=lambda x: x[0], reverse=True)
    seen_texts = set()
    deduped: List[tuple[float, DocumentEmbedding]] = []
    for sim, row in gathered_matches:
        txt = row.text
        if txt in seen_texts:
            continue
        seen_texts.add(txt)
        deduped.append((sim, row))
        if len(deduped) >= (top_k_per_term * 3):
            break

    context_snippets = [r.text for _, r in deduped[:10]]
    context = "\n\n---\n\n".join(context_snippets)

    extraction_prompt = DATA_EXTRACT_PROMPT.format(field_name=field_name, context=context)
    chat_resp = await llm_client.chat(messages=[{"role": "user", "content": extraction_prompt}],
                                      keep_alive=True, format=FieldExtractionResult.model_json_schema())
    content = chat_resp.message.content

    try:
        parsed = FieldExtractionResult.model_validate_json(content)
    except:
        try:
            parsed = FieldExtractionResult.model_validate_json(content.removeprefix('{"'))
        except:
            parsed = FieldExtractionResult.model_validate_json(content.removeprefix('{'))

    print("Parsed: ", parsed)

    try:
        added = await propose_and_add_synonyms(field_name, context_snippets)
        parsed.auto_added_synonyms = added
    except Exception:
        parsed.auto_added_synonyms = []

    return parsed


async def process_document(client, file_path: Path, file_id: int, metadata: Optional[dict] = None) -> (bool, str):
    try:
        text = await extract_pdf_text(client, path=file_path, fileid=file_id)

        await upsert_document_embeddings(file_name=file_path.name, full_text=text, metadata=metadata)
        await upsert_global_embeddings(full_text=text, metadata=metadata)

        return True, ''
    except Exception as e:
        return False, e


__all__ = [
    "process_document", "find_field_value_via_embeddings", "propose_and_add_synonyms", "upsert_document_embeddings",
    "ensure_synonym_embeddings", "upsert_global_embeddings", "get_embeddings", "seed_synonyms",
    "semantic_search_global",
    "semantic_search_local", "chunk_text"
]
