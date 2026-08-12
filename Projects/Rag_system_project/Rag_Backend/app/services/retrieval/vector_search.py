from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


class VectorSearchService:

    def __init__(self, db: Session):
        self.db = db

    def search(
        self,
        query_embedding: list[float],
        limit: int = 5,
    ) -> list[DocumentChunk]:

        if not query_embedding:
            raise ValueError(
                "Query embedding cannot be empty"
            )

        if limit <= 0:
            raise ValueError(
                "Limit must be greater than 0"
            )

        results = (
            self.db.query(DocumentChunk)
            .filter(
                DocumentChunk.embedding.isnot(None)
            )
            .order_by(
                DocumentChunk.embedding.cosine_distance(
                    query_embedding
                )
            )
            .limit(limit)
            .all()
        )

        return results