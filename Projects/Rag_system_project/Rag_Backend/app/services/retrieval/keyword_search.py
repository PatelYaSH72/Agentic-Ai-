from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.models.document import Document


class KeywordSearchService:

    def __init__(self, db: Session):
        self.db = db

    def search(
        self,
        query: str,
        limit: int = 5,
        document_id: int | None = None,
        collection_id: int | None = None,
    ) -> list[DocumentChunk]:

        if not query or not query.strip():
            raise ValueError(
                "Query cannot be empty"
            )

        if limit <= 0:
            raise ValueError(
                "Limit must be greater than 0"
            )

        search_query = query.strip()

        ts_vector = DocumentChunk.chunk_text.op(
            "?"
        )

        query_builder = (
            self.db.query(DocumentChunk)
            .join(
                Document,
                Document.id == DocumentChunk.document_id,
            )
            .filter(
                DocumentChunk.chunk_text.isnot(None)
            )
        )

        # --------------------------------------
        # PostgreSQL Full Text Search
        # --------------------------------------

        from sqlalchemy import func

        vector = func.to_tsvector(
            "english",
            DocumentChunk.chunk_text,
        )

        ts_query = func.plainto_tsquery(
            "english",
            search_query,
        )

        query_builder = query_builder.filter(
            vector.op("@@")(ts_query)
        )

        # --------------------------------------
        # Document filter
        # --------------------------------------

        if document_id is not None:

            query_builder = query_builder.filter(
                DocumentChunk.document_id
                == document_id
            )

        # --------------------------------------
        # Collection filter
        # --------------------------------------

        if collection_id is not None:

            query_builder = query_builder.filter(
                Document.collection_id
                == collection_id
            )

        # --------------------------------------
        # Rank results
        # --------------------------------------

        results = (
            query_builder
            .order_by(
                func.ts_rank(
                    vector,
                    ts_query,
                ).desc()
            )
            .limit(limit)
            .all()
        )

        return results