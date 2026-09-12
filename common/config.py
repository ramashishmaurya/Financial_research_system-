import os
from dotenv import load_dotenv

# Load variables from .env file once
load_dotenv()

class Settings:
    """
    Centralized configuration class.
    Instead of calling os.getenv() in 10 different files, 
    we just import this Settings class everywhere.
    """
    PROJECT_NAME = "Agentic Financial Research"
    
    # API Keys
    GROQ_API_KEY = os.getenv("GROQ_API_KEY")
    TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")
    
    # Database
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./research_engine.db")
    
    # Redis / Celery
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379/0")

# Create a global instance
settings = Settings()
