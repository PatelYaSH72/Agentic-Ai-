from app.core.database import SessionLocal

from app.services.retrieval.retrieval_service import (
    RetrievalService,
)


def test_retrieval_service():

    db = SessionLocal()

    try:

        query = (
            "What is database query optimization?"
        )

        collection_id = 3
        top_k = 5

        print("\n==============================")
        print("RETRIEVAL SERVICE TEST")
        print("==============================")

        print("\nQuery:")
        print(query)

        print("\nCollection ID:")
        print(collection_id)

        print("\nTop-K:")
        print(top_k)

        # --------------------------------------
        # Retrieval Service
        # --------------------------------------

        retrieval_service = (
            RetrievalService(db)
        )

        results = (
            retrieval_service.retrieve(
                query=query,
                limit=top_k,
                collection_id=collection_id,
            )
        )

        # --------------------------------------
        # Results
        # --------------------------------------

        print("\n==============================")
        print("RETRIEVAL RESULTS")
        print("==============================")

        print(
            "\nResults found:",
            len(results),
        )

        assert len(results) <= top_k

        for rank, result in enumerate(
            results,
            start=1,
        ):

            print(
                "\n------------------------------"
            )

            print("Rank:", rank)

            print(
                "Chunk ID:",
                result.id,
            )

            print(
                "Document ID:",
                result.document_id,
            )

            print(
                "Chunk Index:",
                result.chunk_index,
            )

            print(
                "Strategy:",
                result.chunking_strategy,
            )

            print(
                "Text:",
                result.chunk_text[:300],
            )

        print(
            "\n✅ RETRIEVAL SERVICE TEST PASSED"
        )

    finally:

        db.close()


test_retrieval_service()