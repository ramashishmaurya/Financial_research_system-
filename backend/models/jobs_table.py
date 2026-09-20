from sqlalchemy import Column, Integer, String, DateTime, ForeignKey, Enum
from sqlalchemy.orm import relationship
from datetime import datetime
import uuid
import sys
import os
import enum

# Add the parent directory to sys.path so we can import backend.database
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.database import Base

class JobStatus(str, enum.Enum):
    PENDING = "Pending"
    PROCESSING = "Processing"
    COMPLETED = "Completed"
    FAILED = "Failed"

class Job(Base):
    __tablename__ = "jobs"

    # UUID for the job so it's impossible to guess and secure
    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()), index=True)
    
    # User who requested the research (Foreign Key connecting to auth_table)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # What company is being researched
    company_name = Column(String, nullable=False)
    
    # Job tracking status
    status = Column(Enum(JobStatus), default=JobStatus.PENDING)
    
    # The generated Markdown report text (populated when completed)
    report_content = Column(String, nullable=True)
    
    # The AWS S3 URL where the report file is stored
    report_s3_url = Column(String, nullable=True)
    
    # Timestamps
    created_at = Column(DateTime, default=datetime.utcnow)
    completed_at = Column(DateTime, nullable=True)

    # Relationships
    user = relationship("User", backref="jobs")

    def __repr__(self):
        return f"<Job(id='{self.id}', company='{self.company_name}', status='{self.status}')>"
