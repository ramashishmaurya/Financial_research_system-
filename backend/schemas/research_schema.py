from pydantic import BaseModel
from typing import Optional

class ResearchRequest(BaseModel):
    company_name: str

class JobStatusResponse(BaseModel):
    job_id: str
    company_name: str
    status: str
    report_content: Optional[str] = None
