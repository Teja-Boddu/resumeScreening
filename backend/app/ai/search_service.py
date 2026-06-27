from app.ai.qdrant_service import QdrantService


class SearchService:

    @staticmethod
    def search_candidates(
        embedding: list,
        limit: int = 5
    ):

        results = QdrantService.client.query_points(

            collection_name=QdrantService.COLLECTION_NAME,

            query=embedding,

            limit=limit

        )

        return results.points