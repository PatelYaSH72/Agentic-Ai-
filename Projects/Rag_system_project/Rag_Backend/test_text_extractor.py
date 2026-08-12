from app.core.database import SessionLocal

from app.services.retrieval.vector_search import (
    VectorSearchService,
)

from app.services.embedding.embedding_service import (
    EmbeddingService,
)


def test_top_k_retrieval():

    db = SessionLocal()

    try:

        # --------------------------------------
        # Query
        # --------------------------------------

        query = "What is database query optimization?"

        print("\nQuery:")
        print(query)

        # --------------------------------------
        # Query Embedding
        # --------------------------------------

        embedding_service = EmbeddingService()

        query_embedding = (
            embedding_service.generate_embedding(
                query
            )
        )

        print("\nEmbedding dimension:")
        print(len(query_embedding))

        # --------------------------------------
        # Top-K Retrieval
        # --------------------------------------

        top_k = 5

        search_service = VectorSearchService(db)

        results = search_service.search(
            query_embedding=query_embedding,
            limit=top_k,
        )

        # --------------------------------------
        # Validate Top-K
        # --------------------------------------

        print("\n==============================")
        print("TOP-K RETRIEVAL")
        print("==============================")

        print("\nRequested K:", top_k)
        print("Results returned:", len(results))

        assert len(results) <= top_k

        # --------------------------------------
        # Results
        # --------------------------------------

        for index, result in enumerate(
            results,
            start=1,
        ):

            print("\n------------------------------")

            print("Rank:", index)

            print("Chunk ID:", result.id)

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

        print("\n✅ TOP-K RETRIEVAL TEST PASSED")

    finally:

        db.close()


test_top_k_retrieval()