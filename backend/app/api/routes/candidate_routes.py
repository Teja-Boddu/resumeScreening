from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database.postgres import get_db
from app.schemas.candidate_schema import (
    CandidateCreate,
    CandidateResponse
)
from app.services.candidate_service import CandidateService

router = APIRouter()


@router.post(
    "/",
    response_model=CandidateResponse,
    status_code=201
)
def create_candidate(
    candidate: CandidateCreate,
    db: Session = Depends(get_db)
):

    return CandidateService.create_candidate(
        db=db,
        candidate_data=candidate
    )