from qdrant_client import QdrantClient
from qdrant_client.http.models import (
    Distance,
    VectorParams,
    PointStruct
)

from app.core.config import settings


class QdrantService:

    COLLECTION_NAME = "resume_embeddings"

    client = QdrantClient(
        url=settings.QDRANT_URL,
        api_key=settings.QDRANT_API_KEY
    )

    @classmethod
    def create_collection(cls):

        collections = cls.client.get_collections()

        collection_names = [
            collection.name
            for collection in collections.collections
        ]

        if cls.COLLECTION_NAME not in collection_names:

            cls.client.create_collection(
                collection_name=cls.COLLECTION_NAME,
                vectors_config=VectorParams(
                    size=1024,
                    distance=Distance.COSINE
                )
            )

            print("✅ Qdrant Collection Created")

        else:

            print("✅ Collection Already Exists")

    @classmethod
    def store_candidate_embedding(
        cls,
        candidate,
        embedding: list
    ):

        cls.client.upsert(

            collection_name=cls.COLLECTION_NAME,

            points=[

                PointStruct(

                    id=str(candidate.id),

                    vector=embedding,

                    payload={

                        "candidate_id": str(candidate.id),

                        "candidate_name": candidate.full_name,

                        "email": candidate.email,

                        "phone": candidate.phone,

                        "role": candidate.current_role,

                        "experience": candidate.total_experience,

                        "location": candidate.current_location,

                        "skills": candidate.skills,

                        "education": candidate.education,

                        "projects": candidate.projects,

                        "certifications": candidate.certifications,

                        "resume_file": candidate.resume_file_name

                    }

                )

            ]

        )

        print("✅ Embedding Stored Successfully")