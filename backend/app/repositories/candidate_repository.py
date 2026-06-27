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
    
    @staticmethod
    def get_candidate_by_email(
        db: Session,
        email: str
    ):

        return db.query(Candidate).filter(
            Candidate.email == email
        ).first()

    @staticmethod
    def update_candidate(
        db: Session,
        candidate: Candidate,
        candidate_data: CandidateCreate
    ):

        data = candidate_data.model_dump()

        for key, value in data.items():
            setattr(candidate, key, value)

        db.commit()

        db.refresh(candidate)

        return candidate