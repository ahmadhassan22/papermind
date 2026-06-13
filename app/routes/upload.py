from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException
from app.models.schemas import UploadResponse
from app.core.config import UPLOAD_DIR, CHROMA_DIR
from app.utils.file_utils import save_upload_file
from app.services.ingest_service import ingest_document
from langchain_chroma import Chroma
from app.services.ingest_service import get_embedding_model

router = APIRouter()

SUPPORTED_EXTENSIONS = {".pdf", ".docx", ".md", ".txt"}

@router.post("/upload", response_model=UploadResponse)
def upload_document(file: UploadFile = File(...)):
    suffix = Path(file.filename).suffix.lower()
    if suffix not in SUPPORTED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type '{suffix}'. Supported: {', '.join(SUPPORTED_EXTENSIONS)}"
        )
    file_path = Path(UPLOAD_DIR) / file.filename
    save_upload_file(file, file_path)
    ingest_document(file_path)
    return UploadResponse(
        message="File uploaded and indexed successfully.",
        filename=file.filename
    )

@router.get("/documents")
def list_documents():
    try:
        embedding = get_embedding_model()
        vectordb = Chroma(
            persist_directory=str(CHROMA_DIR),
            embedding_function=embedding
        )
        result = vectordb.get()
        metadatas = result.get("metadatas", [])
        filenames = list({m.get("filename", "unknown") for m in metadatas if m})
        return {"documents": sorted(filenames)}
    except Exception:
        return {"documents": []}