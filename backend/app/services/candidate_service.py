from sqlalchemy.orm import Session

from app.repositories.candidate_repository import CandidateRepository
from app.schemas.candidate_schema import CandidateCreate
from app.models.candidate import Candidate


class CandidateService:

    @staticmethod
    def create_candidate(
        db: Session,
        candidate_data: CandidateCreate
    ) -> Candidate:

        return CandidateRepository.create_candidate(
            db=db,
            candidate_data=candidate_data
        )