from sqlalchemy.orm import Session

from app.models.document_chunk import DocumentChunk


class ChunkStorage:

    @staticmethod
    def save_chunks(
        db: Session,
        document_id: int,
        chunks: list[str],
        chunking_strategy: str,
    ) -> list[DocumentChunk]:

        saved_chunks = []

        for index, chunk in enumerate(
            chunks,
            start=1,
        ):

            document_chunk = DocumentChunk(
                document_id=document_id,
                chunk_index=index,
                chunk_text=chunk,
                page_number=None,
                chunk_size=len(chunk),
                chunking_strategy=chunking_strategy,
                embedding_model=None,
                embedding_dimension=None,
                retrieval_count=0,
                average_score=0.0,
            )

            db.add(document_chunk)

            saved_chunks.append(
                document_chunk
            )

        db.commit()

        for chunk in saved_chunks:
            db.refresh(chunk)

        return saved_chunks