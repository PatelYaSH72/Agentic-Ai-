from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk
from app.services.embedding.embedding_service import EmbeddingService


class EmbeddingStorage:

    MODEL_NAME = EmbeddingService.MODEL_NAME
    EMBEDDING_DIMENSION = (
        EmbeddingService.EMBEDDING_DIMENSION
    )

    @staticmethod
    def generate_and_store(
        db: Session,
        document_id: int,
    ) -> int:

        embedding_service = EmbeddingService()

        chunks = (
            db.query(DocumentChunk)
            .filter(
                DocumentChunk.document_id
                == document_id
            )
            .order_by(
                DocumentChunk.chunk_index
            )
            .all()
        )

        if not chunks:
            raise ValueError(
                "No chunks found for this document"
            )

        texts = [
            chunk.chunk_text
            for chunk in chunks
        ]

        embeddings = (
            embedding_service.generate_embeddings(
                texts
            )
        )

        for chunk, embedding in zip(
            chunks,
            embeddings,
        ):

            chunk.embedding = embedding

            chunk.embedding_model = (
                EmbeddingStorage.MODEL_NAME
            )

            chunk.embedding_dimension = (
                EmbeddingStorage.EMBEDDING_DIMENSION
            )

        db.commit()

        return len(chunks)