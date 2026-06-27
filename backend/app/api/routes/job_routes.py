from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.schemas.job_schema import JobDescription
from app.services.job_service import JobService

from app.database.postgres import get_db

router = APIRouter()


@router.post("/match")
def match_candidates(
    job: JobDescription,
    db: Session = Depends(get_db)
):

    return JobService.search_matching_candidates(
        job_description=job.job_description,
        top_k=job.top_k,
        db=db
    )