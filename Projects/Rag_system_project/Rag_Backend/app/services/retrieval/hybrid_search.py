from sqlalchemy.orm import Session

from app.services.embedding.embedding_service import (
    EmbeddingService,
)

from app.services.retrieval.vector_search import (
    VectorSearchService,
)

from app.services.retrieval.keyword_search import (
    KeywordSearchService,
)


class HybridSearchService:

    def __init__(self, db: Session):

        self.db = db

        self.embedding_service = (
            EmbeddingService()
        )

        self.vector_search_service = (
            VectorSearchService(db)
        )

        self.keyword_search_service = (
            KeywordSearchService(db)
        )

    def search(
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

        query = query.strip()

        # --------------------------------------
        # Query Embedding
        # --------------------------------------

        query_embedding = (
            self.embedding_service.generate_embedding(
                query
            )
        )

        # --------------------------------------
        # Vector Search
        # --------------------------------------

        vector_results = (
            self.vector_search_service.search(
                query_embedding=query_embedding,
                limit=limit,
                document_id=document_id,
                collection_id=collection_id,
            )
        )

        # --------------------------------------
        # Keyword Search
        # --------------------------------------

        keyword_results = (
            self.keyword_search_service.search(
                query=query,
                limit=limit,
                document_id=document_id,
                collection_id=collection_id,
            )
        )

        # --------------------------------------
        # Return both result sets
        # --------------------------------------

        return {
            "vector_results": vector_results,
            "keyword_results": keyword_results,
        }