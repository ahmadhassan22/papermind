from langchain_community.vectorstores import Chroma
from langchain_huggingface import HuggingFaceEmbeddings

from app.core.config import CHROMA_DIR, EMBEDDING_MODEL

def get_retriever():
    embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    vectordb = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embedding
    )

    retriever = vectordb.as_retriever(
        search_kwargs={"k": 3}
    )

    return retriever