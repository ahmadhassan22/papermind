import requests
from app.core.config import JINA_API_KEY

def rerank(question: str, docs: list, top_k: int = 5) -> list:
    url = "https://api.jina.ai/v1/rerank"
    headers = {
        "Authorization": f"Bearer {JINA_API_KEY}",
        "Content-Type": "application/json"
    }
    payload = {
        "model": "jina-reranker-v2-base-multilingual",
        "query": question,
        "documents": [doc.page_content for doc in docs],
        "top_n": top_k
    }
    response = requests.post(url, headers=headers, json=payload)
    response.raise_for_status()
    results = response.json()["results"]
    reranked_docs = [docs[r["index"]] for r in results]
    return reranked_docs