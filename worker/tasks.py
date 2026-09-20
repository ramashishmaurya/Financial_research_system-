import time
import sys
import os
from datetime import datetime

# Include the parent directory so we can import the backend package
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from worker.celery_app import celery_app
from backend.database import SessionLocal
from backend.models.jobs_table import Job, JobStatus
from common.aws_utils import upload_to_s3
import tempfile

@celery_app.task(bind=True)
def generate_research_report(self, job_id: str, company_name: str):
    """
    Background worker that runs the Multi-Agent AI System.
    For Phase 2, this simulates the workload with a sleep delay.
    """
    db = SessionLocal()
    try:
        # 1. Update job status to PROCESSING
        job = db.query(Job).filter(Job.id == job_id).first()
        if not job:
            return f"Error: Job {job_id} not found in database."
        
        job.status = JobStatus.PROCESSING
        db.commit()
        print(f"[AI WORKER] Started analyzing: {company_name}")

        # 2. RUN MULTI-AGENT AI SYSTEM (LangGraph)
        from ai_agents.orchestrator import run_research_pipeline
        final_report = run_research_pipeline(company_name)
        
        print(f"[AI WORKER] Finished analyzing: {company_name}. Generating and Uploading Markdown...")

        # 3. Mark job as COMPLETED
        job.status = JobStatus.COMPLETED
        job.completed_at = datetime.utcnow()
        
        # Save the raw Markdown report directly into the database for frontend rendering
        job.report_content = final_report
        
        # 4. Upload to S3
        try:
            # Create a temporary file to hold the markdown content
            with tempfile.NamedTemporaryFile(delete=False, suffix=".md", mode="w", encoding="utf-8") as temp_file:
                temp_file.write(final_report)
                temp_file_path = temp_file.name
            
            s3_file_name = f"reports/report_{job_id}.md"  
            print(f"[AI WORKER] Uploading to S3 as {s3_file_name}...")
            
            s3_url = upload_to_s3(temp_file_path, s3_file_name)
            
            if s3_url:
                job.report_s3_url = s3_url
                print(f"[AI WORKER] S3 Upload successful! URL: {s3_url}")
            else:
                print("[AI WORKER] S3 Upload failed (returned None).")
                
            # Clean up the temp file
            os.remove(temp_file_path)
            
        except Exception as upload_err:
            print(f"[AI WORKER] Error during S3 Upload: {upload_err}")

        db.commit()
        
        return f"Successfully processed report for {company_name}"
    
    except Exception as e:
        db.rollback()
        # Mark as FAILED if something crashes
        job = db.query(Job).filter(Job.id == job_id).first()
        if job:
            job.status = JobStatus.FAILED
            db.commit()
        return f"Failed: {str(e)}"
    finally:
        db.close()


