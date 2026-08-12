from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.models.document import Document


class VectorSearchService:

    def __init__(self, db: Session):
        self.db = db

    def search(
        self,
        query_embedding: list[float],
        limit: int = 5,
        document_id: int | None = None,
        collection_id: int | None = None,
    ) -> list[DocumentChunk]:

        if not query_embedding:
            raise ValueError(
                "Query embedding cannot be empty"
            )

        if limit <= 0:
            raise ValueError(
                "Limit must be greater than 0"
            )

        query = (
            self.db.query(DocumentChunk)
            .join(
                Document,
                Document.id == DocumentChunk.document_id,
            )
            .filter(
                DocumentChunk.embedding.isnot(None)
            )
        )

        # --------------------------------------
        # Document filter
        # --------------------------------------

        if document_id is not None:

            query = query.filter(
                DocumentChunk.document_id == document_id
            )

        # --------------------------------------
        # Collection filter
        # --------------------------------------

        if collection_id is not None:

            query = query.filter(
                Document.collection_id == collection_id
            )

        # --------------------------------------
        # Vector similarity + Top-K
        # --------------------------------------

        results = (
            query
            .order_by(
                DocumentChunk.embedding.cosine_distance(
                    query_embedding
                )
            )
            .limit(limit)
            .all()
        )

        return results