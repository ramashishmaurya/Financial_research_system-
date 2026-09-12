from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime
import sys
import os

# Add the parent directory to sys.path so we can import backend.database
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../..')))

from backend.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    reports_generated = Column(Integer, default=0)

    def __repr__(self):
        return f"<User(email='{self.email}', reports_generated={self.reports_generated})>"
