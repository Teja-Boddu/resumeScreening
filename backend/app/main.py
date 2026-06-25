from fastapi import FastAPI

from app.api.router import api_router

from app.database.base import Base
from app.database.postgres import engine

# Import models
from app.models.candidate import Candidate

Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="AI-Powered Intelligent Recruitment & Resume Screening Platform",
    version="1.0.0"
)

app.include_router(api_router)