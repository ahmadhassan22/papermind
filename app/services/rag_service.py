from ollama import chat
from app.services.retrieval_service import get_retriever


def answer_question(question: str):
    retriever = get_retriever()
    docs = retriever.invoke(question)

    context = "\n\n".join([doc.page_content for doc in docs])
    sources = [doc.metadata.get("source", "unknown") for doc in docs]

    prompt = f"""
You are a helpful assistant.
Answer the user's question only using the provided context.
If the answer is not in the context, say: "I could not find the answer in the uploaded document."

Context:
{context}

Question:
{question}

Answer:
"""

    response = chat(
        model="phi3",
        messages=[{"role": "user", "content": prompt}]
    )

    answer = response["message"]["content"]
    return answer, sources