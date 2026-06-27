# from sqlalchemy.orm import Session

# from app.ai.matching_pipeline import MatchingPipeline


# class JobService:

#     @staticmethod
#     def search_matching_candidates(
#         job_description: str,
#         top_k: int,
#         db: Session
#     ):

#         candidates = MatchingPipeline.run(
#             job_description=job_description,
#             top_k=top_k,
#             db=db
#         )

#         response = []

#         rank = 1

#         for candidate in candidates:

#             response.append({

#                 "rank": rank,

#                 "semantic_score": candidate.semantic_score,

#                 "candidate_id": str(candidate.id),

#                 "candidate_name": candidate.full_name,

#                 "email": candidate.email,

#                 "phone": candidate.phone,

#                 "current_role": candidate.current_role,

#                 "experience": candidate.total_experience,

#                 "skills": candidate.skills,

#                 "professional_summary": candidate.professional_summary

#             })

#             rank += 1

#         return response













from sqlalchemy.orm import Session

from app.ai.matching_pipeline import MatchingPipeline


class JobService:

    @staticmethod
    def search_matching_candidates(
        job_description: str,
        top_k: int,
        db: Session
    ):

        return MatchingPipeline.run(

            job_description=job_description,

            top_k=top_k,

            db=db

        )