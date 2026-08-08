from app.core.database import SessionLocal

from app.services.processing.embedding_storage import (
    EmbeddingStorage,
)


DOCUMENT_ID = 1


db = SessionLocal()

try:

    count = EmbeddingStorage.generate_and_store(
        db=db,
        document_id=DOCUMENT_ID,
    )

    print(
        f"Embeddings stored: {count}"
    )

finally:

    db.close()