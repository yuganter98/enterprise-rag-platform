import os
import pandas as pd
from sqlalchemy.orm import Session
from datetime import datetime
from typing import Optional

from app.core.config import settings
from app.models.employee import Employee

REPORT_DIR = os.path.join(os.path.abspath(settings.DATA_DIR), "reports")

def generate_employee_report(db: Session, filters: dict) -> Optional[str]:
    """
    Generates an Excel report of employees based on filters.
    Returns the absolute file path of the generated report,
    or None if no employees match the filters.
    """
    if not os.path.exists(REPORT_DIR):
        os.makedirs(REPORT_DIR)

    query = db.query(Employee)
    
    # Apply filters (simple equality for now, expand as needed)
    if "department" in filters:
        query = query.filter(Employee.department == filters["department"])
    if "designation" in filters:
        query = query.filter(Employee.designation == filters["designation"])
        
    employees = query.all()
    
    if not employees:
        return None

    # Convert to DataFrame
    data = []
    for emp in employees:
        data.append({
            "ID": emp.id,
            "Name": f"{emp.first_name} {emp.last_name}",
            "Department": emp.department,
            "Designation": emp.designation
        })
    
    df = pd.DataFrame(data)
    
    # Generate filename
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"employee_report_{timestamp}.xlsx"
    file_path = os.path.join(REPORT_DIR, filename)
    
    # Save
    df.to_excel(file_path, index=False)
    
    return file_path
