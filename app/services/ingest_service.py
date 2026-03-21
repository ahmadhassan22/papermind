from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

from app.core.config import CHROMA_DIR, EMBEDDING_MODEL

def ingest_pdf(file_path: Path) -> None:
    # 1. Load PDF
    loader = PyPDFLoader(str(file_path))
    docs = loader.load()

    # 2. Split into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size = 500,
        chunk_overlap = 100
    )

    chunks = splitter.split_documents(docs)

    # 3. Create embeddings
    embedding = HuggingFaceEmbeddings(model_name=EMBEDDING_MODEL)

    # 4. Store in vector database
    Chroma.from_documents(
        documents=chunks,
        embedding=embedding,
        persist_directory=str(CHROMA_DIR)
    )