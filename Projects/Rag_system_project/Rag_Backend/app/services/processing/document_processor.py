from sqlalchemy.orm import Session

from app.models.document import Document
from app.models.document_chunk import DocumentChunk

from app.services.processing.text_extractor import TextExtractor
from app.services.processing.chunking_factory import ChunkingFactory
from app.services.embedding.embedding_service import EmbeddingService


class DocumentProcessor:

    def __init__(self):
        self.text_extractor = TextExtractor()
        self.embedding_service = EmbeddingService()

    def process_document(
        self,
        document: Document,
        db: Session,
        chunking_strategy: str = "recursive",
    ):

        # --------------------------------------
        # 1. Update processing status
        # --------------------------------------

        document.processing_status = "processing"
        db.commit()

        try:

            # ----------------------------------
            # 2. Extract text
            # ----------------------------------

            text = self.text_extractor.extract_text(
                document.file_path
            )

            if not text or not text.strip():
                raise ValueError(
                    "No text could be extracted from document"
                )

            # ----------------------------------
            # 3. Select chunking strategy
            # ----------------------------------

            chunker = ChunkingFactory.get_chunker(
                chunking_strategy
            )

            chunks = chunker.split_text(text)

            if not chunks:
                raise ValueError(
                    "No chunks were generated"
                )

            # ----------------------------------
            # 4. Remove old chunks
            # ----------------------------------

            db.query(DocumentChunk).filter(
                DocumentChunk.document_id == document.id
            ).delete(
                synchronize_session=False
            )

            # ----------------------------------
            # 5. Generate embeddings + save
            # ----------------------------------

            for index, chunk_text in enumerate(chunks):

                chunk_text = chunk_text.strip()

                if not chunk_text:
                    continue

                embedding = (
                    self.embedding_service
                    .generate_embedding(chunk_text)
                )

                chunk = DocumentChunk(

                    document_id=document.id,

                    chunk_index=index,

                    chunk_text=chunk_text,

                    page_number=None,

                    chunk_size=len(chunk_text),

                    chunking_strategy=(
                        chunking_strategy
                    ),

                    embedding_model=(
                        self.embedding_service.MODEL_NAME
                    ),

                    embedding_dimension=len(
                        embedding
                    ),

                    retrieval_count=0,

                    average_score=0.0,

                    embedding=embedding,
                )

                db.add(chunk)

            # ----------------------------------
            # 6. Update document
            # ----------------------------------

            document.is_processed = True

            document.processing_status = "completed"

            db.commit()

            db.refresh(document)

            return {
                "document_id": document.id,
                "chunks_created": len(chunks),
                "chunking_strategy": (
                    chunking_strategy
                ),
                "processing_status": (
                    document.processing_status
                ),
            }

        except Exception:

            db.rollback()

            document.processing_status = "failed"

            db.commit()

            raise