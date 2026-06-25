from fastapi import APIRouter

from app.api.routes.health_routes import router as health_router
from app.api.routes.candidate_routes import router as candidate_router
from app.api.routes.job_routes import router as job_router
from app.api.routes.analysis_routes import router as analysis_router
from app.api.routes.resume_routes import router as resume_router

api_router = APIRouter()

api_router.include_router(
    health_router,
    tags=["Health"]
)

api_router.include_router(
    candidate_router,
    prefix="/candidates",
    tags=["Candidates"]
)

api_router.include_router(
    job_router,
    prefix="/jobs",
    tags=["Jobs"]
)

api_router.include_router(
    analysis_router,
    prefix="/analysis",
    tags=["Analysis"]
)

api_router.include_router(
    resume_router,
    prefix="/resume",
    tags=["Resume"]
)