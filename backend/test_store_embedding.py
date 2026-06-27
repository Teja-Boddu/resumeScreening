from app.ai.embedding_service import EmbeddingService
from app.ai.qdrant_service import QdrantService

embedding = EmbeddingService.generate_embedding(
    "Python FastAPI PostgreSQL Backend Developer"
)

QdrantService.store_candidate_embedding(
    candidate_id="1",
    candidate_name="John Doe",
    embedding=embedding
)