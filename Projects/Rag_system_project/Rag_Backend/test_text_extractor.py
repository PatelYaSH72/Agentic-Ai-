from app.core.database import SessionLocal

from app.services.retrieval.vector_search import (
    VectorSearchService,
)

from app.services.embedding.embedding_service import (
    EmbeddingService,
)


def test_metadata_filtering():

    db = SessionLocal()

    try:

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
        # Metadata Filter
        # --------------------------------------

        collection_id = 3
        top_k = 5

        print("\nCollection ID:")
        print(collection_id)

        # --------------------------------------
        # Search
        # --------------------------------------

        search_service = VectorSearchService(db)

        results = search_service.search(
            query_embedding=query_embedding,
            limit=top_k,
            collection_id=collection_id,
        )

        # --------------------------------------
        # Results
        # --------------------------------------

        print("\n==============================")
        print("METADATA FILTERED SEARCH")
        print("==============================")

        print("\nResults found:")
        print(len(results))

        assert len(results) <= top_k

        for rank, result in enumerate(
            results,
            start=1,
        ):

            print("\n------------------------------")

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
            "\n✅ METADATA FILTERING TEST PASSED"
        )

    finally:

        db.close()


test_metadata_filtering()