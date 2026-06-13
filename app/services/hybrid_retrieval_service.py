from langchain_chroma import Chroma
from langchain_core.documents import Document
from app.services.ingest_service import get_embedding_model
from app.core.config import CHROMA_DIR
from rank_bm25 import BM25Okapi

def get_all_docs():
    embedding = get_embedding_model()
    vectordb = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embedding
    )
    result = vectordb.get()
    documents = result["documents"]
    metadatas = result["metadatas"]
    return documents, metadatas

def bm25_search(query: str, documents: list, metadatas: list, top_k: int = 20) -> list:
    tokenized_docs = [doc.lower().split() for doc in documents]
    bm25 = BM25Okapi(tokenized_docs)
    tokenized_query = query.lower().split()
    scores = bm25.get_scores(tokenized_query)
    top_indices = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:top_k]
    return [(documents[i], metadatas[i], scores[i]) for i in top_indices]

def reciprocal_rank_fusion(dense_docs, bm25_results, k: int = 60) -> list:
    scores = {}
    for rank, doc in enumerate(dense_docs):
        key = doc.page_content[:100]
        scores[key] = scores.get(key, {"doc": doc, "score": 0})
        scores[key]["score"] += 1 / (k + rank + 1)
    for rank, (text, metadata, _) in enumerate(bm25_results):
        key = text[:100]
        if key not in scores:
            scores[key] = {
                "doc": Document(page_content=text, metadata=metadata),
                "score": 0
            }
        scores[key]["score"] += 1 / (k + rank + 1)
    sorted_results = sorted(scores.values(), key=lambda x: x["score"], reverse=True)
    return [item["doc"] for item in sorted_results]

def hybrid_retrieve(query: str, top_k: int = 20) -> list:
    embedding = get_embedding_model()
    vectordb = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embedding
    )
    dense_docs = vectordb.similarity_search(query, k=top_k)
    documents, metadatas = get_all_docs()
    bm25_results = bm25_search(query, documents, metadatas, top_k=top_k)
    fused = reciprocal_rank_fusion(dense_docs, bm25_results)
    return fused[:top_k]