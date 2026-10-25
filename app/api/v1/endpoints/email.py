from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.email import EmailRequest
from app.services.email.sender import send_email

router = APIRouter()

@router.post("/send")
def send_email_endpoint(
    request: EmailRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Send an email. 
    RBAC rules for mass emails are handled within the service layer.
    """
    try:
        status_msg = send_email(
            db, 
            current_user, 
            request.to_email, 
            request.subject, 
            request.body
        )
        return {"message": status_msg}
    except PermissionError as e:
        # Catch the RBAC error from service and return 403
        raise HTTPException(status_code=403, detail=str(e)) from e
