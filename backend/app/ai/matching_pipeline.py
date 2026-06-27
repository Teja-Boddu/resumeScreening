from sqlalchemy.orm import Session

from app.ai.embedding_service import EmbeddingService
from app.ai.search_service import SearchService
from app.ai.reranker_service import RerankerService
from app.ai.scoring_service import ScoringService
from app.ai.recruiter_report import RecruiterReport

from app.services.candidate_service import CandidateService


class MatchingPipeline:

    @staticmethod
    def run(
        job_description: str,
        top_k: int,
        db: Session
    ):

        # ----------------------------------
        # Step 1 Generate Job Embedding
        # ----------------------------------

        job_embedding = EmbeddingService.generate_embedding(
            job_description
        )

        # ----------------------------------
        # Step 2 Semantic Search
        # ----------------------------------

        search_results = SearchService.search_candidates(
            embedding=job_embedding,
            limit=20
        )

        candidates = []

        for result in search_results:

            candidate = CandidateService.get_candidate_by_id(
                db=db,
                candidate_id=result.payload["candidate_id"]
            )

            if candidate is None:
                continue

            candidates.append({

                "candidate": candidate,

                "semantic_score": round(
                    result.score * 100,
                    2
                )

            })

        # ----------------------------------
        # Step 3 Cross Encoder Reranking
        # ----------------------------------

        reranked = RerankerService.rerank(

            job_description,

            [item["candidate"] for item in candidates]

        )

        semantic_map = {

            item["candidate"].id: item["semantic_score"]

            for item in candidates

        }

        response = []

        # ----------------------------------
        # Step 4 Hybrid Scoring
        # ----------------------------------

        for item in reranked:

            candidate = item["candidate"]

            reranker_score = item["reranker_score"]

            semantic_score = semantic_map[candidate.id]

            skill_score = ScoringService.skill_score(
                job_description,
                candidate
            )

            experience_score = ScoringService.experience_score(
                job_description,
                candidate
            )

            education_score = ScoringService.education_score(
                job_description,
                candidate
            )

            final_score = ScoringService.final_score(

                semantic=semantic_score,

                reranker=reranker_score,

                skill=skill_score,

                experience=experience_score,

                education=education_score

            )

            # ----------------------------------
            # Step 5 AI Recruiter Report
            # ----------------------------------

            report = RecruiterReport.generate_report(

                job_description,

                candidate

            )

            response.append({

                "rank": 0,

                "candidate_id": str(candidate.id),

                "candidate_name": candidate.full_name,

                "email": candidate.email,

                "phone": candidate.phone,

                "current_role": candidate.current_role,

                "experience": candidate.total_experience,

                "skills": candidate.skills,

                "semantic_score": semantic_score,

                "reranker_score": round(
                    reranker_score,
                    2
                ),

                "skill_score": skill_score,

                "experience_score": experience_score,

                "education_score": education_score,

                "final_score": final_score,

                "recommendation": report.get(
                    "recommendation",
                    ""
                ),

                "strengths": report.get(
                    "strengths",
                    []
                ),

                "missing_skills": report.get(
                    "missing_skills",
                    []
                ),

                "summary": report.get(
                    "summary",
                    ""
                )

            })

        # ----------------------------------
        # Step 6 Final Ranking
        # ----------------------------------

        response.sort(

            key=lambda x: x["final_score"],

            reverse=True

        )

        for index, item in enumerate(response):

            item["rank"] = index + 1

        return response[:top_k]