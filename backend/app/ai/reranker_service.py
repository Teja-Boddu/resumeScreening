from sentence_transformers import CrossEncoder


class RerankerService:

    _model = None

    @classmethod
    def get_model(cls):

        if cls._model is None:

            print("Loading BGE Reranker...")

            cls._model = CrossEncoder(
                "BAAI/bge-reranker-v2-m3"
            )

            print("BGE Reranker Loaded")

        return cls._model

    @classmethod
    def rerank(
        cls,
        job_description: str,
        candidates: list
    ):

        model = cls.get_model()

        sentence_pairs = []

        for candidate in candidates:

            document = f"""
Role:
{candidate.current_role}

Experience:
{candidate.total_experience}

Professional Summary:
{candidate.professional_summary}

Skills:
{", ".join(candidate.skills or [])}

Education:
{candidate.education}

Projects:
{candidate.projects}

Certifications:
{candidate.certifications}
"""

            sentence_pairs.append(
                (
                    job_description,
                    document
                )
            )

        scores = model.predict(
            sentence_pairs
        )

        reranked = []

        for candidate, score in zip(
            candidates,
            scores
        ):

            reranked.append({

                "candidate": candidate,

                "reranker_score": float(score)

            })

        reranked.sort(
            key=lambda x: x["reranker_score"],
            reverse=True
        )

        return reranked