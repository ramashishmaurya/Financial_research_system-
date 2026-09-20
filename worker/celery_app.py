import os
from dotenv import load_dotenv
from celery import Celery

load_dotenv()

# Fallback to local Redis if env variable is not set
REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0") 

celery_app = Celery(
    "research_worker",
    broker=REDIS_URL,
    backend=REDIS_URL,
    include=["worker.tasks"]
)

# Basic Celery Config
celery_app.conf.update(
    task_serializer="json",
    accept_content=["json"],
    result_serializer="json",
    timezone="Asia/Kolkata",
    enable_utc=True,
)
