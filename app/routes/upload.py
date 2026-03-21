from pathlib import Path
from fastapi import APIRouter, UploadFile, File, HTTPException

from app.models.schemas import UploadResponse
from app.core.config import UPLOAD_DIR
from app.utils.file_utils import save_upload_file
from app.services.ingest_service import ingest_pdf

router = APIRouter()

@router.post("/upload", response_model=UploadResponse)
def upload_document(file: UploadFile = File(...)):
    if not file.filename.lower().endswith(".pdf"):
        raise HTTPException(status_code=400, detail="Only PDF files are supported.")
    
    file_path = Path(UPLOAD_DIR) / file.filename
    save_upload_file(file, file_path)

    ingest_pdf(file_path)

    return UploadResponse(
        message="File uploaded successfully.",
        filename=file.filename
    )