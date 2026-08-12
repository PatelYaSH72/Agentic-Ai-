from sqlalchemy.orm import Session

from app.services.embedding.embedding_service import (
    EmbeddingService,
)

from app.services.retrieval.vector_search import (
    VectorSearchService,
)


class RetrievalService:

    def __init__(self, db: Session):

        self.db = db

        self.embedding_service = (
            EmbeddingService()
        )

        self.vector_search_service = (
            VectorSearchService(db)
        )

    def retrieve(
        self,
        query: str,
        limit: int = 5,
        document_id: int | None = None,
        collection_id: int | None = None,
    ):

        # --------------------------------------
        # Validate query
        # --------------------------------------

        if not query or not query.strip():

            raise ValueError(
                "Query cannot be empty"
            )

        if limit <= 0:

            raise ValueError(
                "Limit must be greater than 0"
            )

        # --------------------------------------
        # Generate query embedding
        # --------------------------------------

        query_embedding = (
            self.embedding_service.generate_embedding(
                query
            )
        )

        # --------------------------------------
        # Vector Search
        # --------------------------------------

        results = (
            self.vector_search_service.search(
                query_embedding=query_embedding,
                limit=limit,
                document_id=document_id,
                collection_id=collection_id,
            )
        )

        return results