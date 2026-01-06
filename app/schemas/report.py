from typing import Optional, Dict
from pydantic import BaseModel

class ReportRequest(BaseModel):
    filters: Optional[Dict[str, str]] = {}
