from app.services.retrieval_service import get_retriever

question = "What is Alif about?"

retriever = get_retriever()
docs = retriever.invoke(question)

for i, doc in enumerate(docs, start=1):
    print(f"\n-- Result {i} ---")
    print(doc.page_content[:500])
    print(doc.metadata)