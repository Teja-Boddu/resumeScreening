from fastapi import APIRouter

from app.api.routes import (
    health_routes,
    resume_routes,
    candidate_routes,
    analysis_routes,
    job_routes
)



api_router = APIRouter()

api_router.include_router(
    health_routes.router,
    prefix="/health",
    tags=["Health"]
)

api_router.include_router(
    resume_routes.router,
    prefix="/resume",
    tags=["Resume"]
)

api_router.include_router(
    candidate_routes.router,
    prefix="/candidate",
    tags=["Candidate"]
)

api_router.include_router(
    analysis_routes.router,
    prefix="/analysis",
    tags=["Analysis"]
)

api_router.include_router(
    job_routes.router,
    prefix="/job",
    tags=["Job Matching"]
)

