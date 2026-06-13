from langchain_chroma import Chroma
from app.core.config import CHROMA_DIR
from app.services.ingest_service import get_embedding_model

def get_retriever():
    embedding = get_embedding_model()
    vectordb = Chroma(
        persist_directory=str(CHROMA_DIR),
        embedding_function=embedding
    )
    retriever = vectordb.as_retriever(
        search_kwargs={"k": 20}
    )
    return retriever