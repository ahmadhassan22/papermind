import re
from groq import Groq
from app.services.hybrid_retrieval_service import hybrid_retrieve
from app.services.rerank_service import rerank
from app.core.config import GROQ_API_KEY, GROQ_MODEL

_client = None

def get_client():
    global _client
    if _client is None:
        _client = Groq(api_key=GROQ_API_KEY)
    return _client

def clean_text(text: str, max_length: int = 300) -> str:
    text = re.sub(r'-\s*\n\s*', '', text)
    text = text.replace("\n", " ").replace("\r", " ")
    text = re.sub(r'(\d+\.)([A-Z])', r'\1 \2', text)
    text = " ".join(text.split())
    if len(text) > max_length:
        cut = text[:max_length]
        last_space = cut.rfind(" ")
        text = cut[:last_space] + "..."
    return text

def answer_question(question: str):
    docs = hybrid_retrieve(question, top_k=20)
    docs = rerank(question, docs, top_k=5)

    context_parts = []
    sources = []

    for i, doc in enumerate(docs):
        filename = doc.metadata.get("filename", "unknown")
        page = doc.metadata.get("page", 0)
        page_display = int(page) + 1
        clean_content = clean_text(doc.page_content, max_length=99999)
        context_parts.append(
            f"[{i+1}] (Source: {filename}, Page: {page_display})\n{clean_content}"
        )
        sources.append({
            "index": i + 1,
            "filename": filename,
            "page": page_display,
            "snippet": clean_text(doc.page_content, max_length=300)
        })

    context = "\n\n".join(context_parts)

    prompt = f"""You are a research assistant helping users understand academic papers.
Answer the question using only the provided context.
Each context chunk is numbered with its source file and page number.
When you use information from a chunk, cite it inline like [1], [2], etc.
Only cite chunks that directly support your answer.
If the answer is not in the context, say: "I could not find the answer in the uploaded documents."

Context:
{context}

Question:
{question}

Answer:"""

    try:
        response = get_client().chat.completions.create(
            model=GROQ_MODEL,
            messages=[{"role": "user", "content": prompt}],
            temperature=0.2,
            timeout=30
        )
        answer = response.choices[0].message.content
    except Exception as e:
        return f"Error generating answer: {str(e)}", []

    cited_indices = set(int(x) for x in re.findall(r'\[(\d+)\]', answer))
    filtered_sources = [s for s in sources if s["index"] in cited_indices]

    return answer, filtered_sources