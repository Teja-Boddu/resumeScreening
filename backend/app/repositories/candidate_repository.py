from sqlalchemy.orm import Session

from app.models.candidate import Candidate
from app.schemas.candidate_schema import CandidateCreate


class CandidateRepository:

    @staticmethod
    def create_candidate(
        db: Session,
        candidate_data: CandidateCreate
    ) -> Candidate:

        candidate = Candidate(
            **candidate_data.model_dump()
        )

        db.add(candidate)

        db.commit()

        db.refresh(candidate)

        return candidate