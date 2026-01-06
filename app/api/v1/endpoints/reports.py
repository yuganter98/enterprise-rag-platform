from typing import Any
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api import deps
from app.models.user import User
from app.schemas.report import ReportRequest
from app.services.report.excel import generate_employee_report
from app.core.rbac import has_role

router = APIRouter()

@router.post("/employees")
def generate_report(
    request: ReportRequest,
    db: Session = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """
    Generate an Excel report of employees. RESTRICTED to HR/Admin.
    """
    if not (has_role(current_user, "hr") or has_role(current_user, "admin")):
        raise HTTPException(status_code=403, detail="Not authorized to generate reports")

    file_path = generate_employee_report(db, request.filters)
    return {"message": "Report generated", "file_path": file_path}
