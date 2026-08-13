from app.services.embedding.embedding_service import (
    EmbeddingService,
)




class QueryEmbeddingService:

    def __init__(
        self,
        embedding_service: EmbeddingService,
    ):
        self.embedding_service = embedding_service

    def generate(
        self,
        query: str,
    ) -> list[float]:

        if not query or not query.strip():

            raise ValueError(
                "Query cannot be empty"
            )

        query = query.strip()

        embedding = (
            self.embedding_service.generate_embedding(
                query
            )
        )

        if len(embedding) != 384:

            raise ValueError(
                "Invalid query embedding dimension"
            )

        return embedding