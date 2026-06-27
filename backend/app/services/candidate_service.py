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

    @staticmethod
    def get_candidate_by_email(
        db: Session,
        email: str
    ):

        return CandidateRepository.get_candidate_by_email(
            db=db,
            email=email
        )


    @staticmethod
    def update_candidate(
        db: Session,
        candidate,
        candidate_data
    ):

        return CandidateRepository.update_candidate(
            db=db,
            candidate=candidate,
            candidate_data=candidate_data
        )

    @staticmethod
    def get_candidate_by_id(
        db: Session,
        candidate_id: str
    ):

        return db.query(Candidate).filter(
            Candidate.id == candidate_id
        ).first()

    @staticmethod
    def get_resume_path(
        db: Session,
        candidate_id: str
    ):

        candidate = CandidateService.get_candidate_by_id(
            db=db,
            candidate_id=candidate_id
        )

        if candidate is None:
            return None

        return candidate.resume_path