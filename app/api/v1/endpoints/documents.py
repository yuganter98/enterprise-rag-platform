import os
import shutil
from typing import Any
from fastapi import APIRouter, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.models.document import Document
from app.services.rag.service import ingest_document

router = APIRouter()

UPLOAD_DIR = os.path.join(os.getcwd(), "data", "uploads")
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Upload a document (PDF/TXT) and ingest it into the RAG system.
    """
    # 1. Save file to disk
    file_location = os.path.join(UPLOAD_DIR, file.filename)
    with open(file_location, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)
    
    # 2. Get Role
    role_name = current_user.role.name if current_user.role else "employee"
    
    # 3. Ingest
    try:
        num_chunks = ingest_document(
            file_location, 
            title=file.filename, 
            user_id=current_user.id, 
            role=role_name
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ingestion failed: {str(e)}")

    # 4. Save metadata to DB
    doc = Document(
        title=file.filename,
        file_path=file_location,
        uploaded_by=current_user.id
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    return {"message": "Document uploaded and ingested successfully", "chunks": num_chunks, "id": doc.id}
