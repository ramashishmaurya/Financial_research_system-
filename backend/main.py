from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.database import engine, Base
from backend.models import auth_table, jobs_table
from backend.routes import research_routes

# Create the database tables if they don't exist
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Multi-Agent Financial Research System",
    description="Asynchronous API for AI-driven market research",
    version="1.0.0"
)

# Enable CORS for the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins for local testing
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(research_routes.router, prefix="/api/v1", tags=["Research"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the Agentic Research Engine API"}

@app.get("/health")
def health_check():
    return {"status": "ok", "db": "connected"}
