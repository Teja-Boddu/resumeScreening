import requests

OLLAMA_URL = "http://localhost:11434/api/embeddings"


class EmbeddingService:

    MODEL_NAME = "bge-m3:latest"

    @classmethod
    def generate_embedding(cls, text: str):

        response = requests.post(
            OLLAMA_URL,
            json={
                "model": cls.MODEL_NAME,
                "prompt": text
            }
        )

        response.raise_for_status()

        embedding = response.json()["embedding"]

        return embedding