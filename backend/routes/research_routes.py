from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from backend.database import get_db
from backend.models.jobs_table import Job
from backend.schemas.research_schema import ResearchRequest, JobStatusResponse
from worker.tasks import generate_research_report

router = APIRouter()

@router.post("/research", response_model=JobStatusResponse)
def start_research(request: ResearchRequest, db: Session = Depends(get_db)):
    """
    Accepts a company name, creates a Job in the DB, and fires the background worker.
    """
    # 1. Create a Pending Job in Database
    # Note: For now, we mock the user_id as 1 (Assuming a logged in user with ID=1)
    # In a real scenario, user_id comes from JWT token dependencies.
    new_job = Job(user_id=1, company_name=request.company_name)
    db.add(new_job)
    db.commit()
    db.refresh(new_job)

    # 2. Fire the Celery Task Asynchronously
    # We pass the job_id (UUID) and the company_name to the worker
    generate_research_report.delay(new_job.id, new_job.company_name)

    # 3. Return the Job ID immediately to the user
    return JobStatusResponse(
        job_id=new_job.id,
        company_name=new_job.company_name,
        status=new_job.status,
        report_content=None
    )

@router.get("/status/{job_id}", response_model=JobStatusResponse)
def get_job_status(job_id: str, db: Session = Depends(get_db)):
    """
    Allows the user to poll the status of their report generation.
    """
    job = db.query(Job).filter(Job.id == job_id).first()
    if not job:
        raise HTTPException(status_code=404, detail="Job not found")

    return JobStatusResponse(
        job_id=job.id,
        company_name=job.company_name,
        status=job.status,
        report_content=job.report_content
    )
