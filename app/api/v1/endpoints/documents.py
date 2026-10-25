import os
import re
import uuid
from typing import Any
from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.core.config import settings
from app.models.user import User
from app.models.document import Document
from app.models.role import Role
from app.services.rag.service import ingest_document

router = APIRouter()

UPLOAD_DIR = os.path.join(os.getcwd(), "data", "uploads")
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

ALLOWED_EXTENSIONS = {".pdf", ".txt", ".docx", ".csv", ".xlsx"}
CHUNK_SIZE = 1024 * 1024


def sanitize_filename(filename: str) -> str:
    """
    Strips any directory components and unsafe characters from a client-supplied
    filename so it can't escape UPLOAD_DIR (e.g. "../../app/main.py").
    """
    name = os.path.basename(filename.replace("\\", "/"))
    name = re.sub(r"[^A-Za-z0-9._ -]", "_", name).strip(" .")
    return name or "upload"

@router.post("/upload")
def upload_document(
    file: UploadFile = File(...),
    allowed_roles: str = Form(
        "",
        description="Comma-separated role names that may retrieve this document. Empty means all roles.",
    ),
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_admin_user),
) -> Any:
    """
    Upload a document (PDF/TXT/DOCX/CSV/XLSX) and ingest it into the RAG system. (Admin only)
    """
    original_name = sanitize_filename(file.filename or "")
    ext = os.path.splitext(original_name)[1].lower()
    if ext not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Unsupported file type. Allowed: {', '.join(sorted(ALLOWED_EXTENSIONS))}",
        )

    # 0. Resolve who can see this document
    all_roles = [r.name for r in db.query(Role).all()]
    requested = [r.strip() for r in allowed_roles.split(",") if r.strip()]
    unknown = set(requested) - set(all_roles)
    if unknown:
        raise HTTPException(status_code=400, detail=f"Unknown roles: {', '.join(sorted(unknown))}")
    visible_to = requested or all_roles

    # 1. Save file to disk under a unique name (never overwrite existing uploads),
    #    enforcing the size limit while streaming.
    file_location = os.path.join(UPLOAD_DIR, f"{uuid.uuid4().hex}_{original_name}")
    max_bytes = settings.MAX_UPLOAD_SIZE_MB * 1024 * 1024
    written = 0
    with open(file_location, "wb") as buffer:
        while chunk := file.file.read(CHUNK_SIZE):
            written += len(chunk)
            if written > max_bytes:
                break
            buffer.write(chunk)
    if written > max_bytes:
        os.remove(file_location)
        raise HTTPException(status_code=413, detail=f"File exceeds {settings.MAX_UPLOAD_SIZE_MB} MB limit")
    
    # 2. Get Role
    role_name = current_user.role.name if current_user.role else "employee"
    
    # 3. Ingest
    try:
        num_chunks = ingest_document(
            file_location, 
            title=original_name,
            user_id=current_user.id, 
            role=role_name,
            allowed_roles=visible_to,
        )
    except Exception as e:
        os.remove(file_location)
        print(f"[Documents] Ingestion failed for {original_name}: {e}")
        raise HTTPException(status_code=422, detail="Could not process this document. Check that the file is valid.")

    # 4. Save metadata to DB
    doc = Document(
        title=original_name,
        file_path=file_location,
        file_type=ext.lstrip("."),
        uploaded_by=current_user.id
    )
    db.add(doc)
    db.commit()
    db.refresh(doc)
    
    return {"message": "Document uploaded and ingested successfully", "chunks": num_chunks, "id": doc.id, "allowed_roles": visible_to}
