from app.ai.embedding_service import EmbeddingService

embedding = EmbeddingService.generate_embedding(
    "Python FastAPI PostgreSQL Backend Developer"
)

print(type(embedding))
print(len(embedding))