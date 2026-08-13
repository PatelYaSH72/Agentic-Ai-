from app.services.embedding.embedding_service import (
    EmbeddingService,
)

from app.services.retrieval.query_embedding import (
    QueryEmbeddingService,
)


def test_query_embedding():

    # --------------------------------------
    # Initialize services
    # --------------------------------------

    embedding_service = EmbeddingService()

    query_embedding_service = (
        QueryEmbeddingService(
            embedding_service
        )
    )

    # --------------------------------------
    # Test Query
    # --------------------------------------

    query = (
        "What is database query optimization?"
    )

    # --------------------------------------
    # Generate Query Embedding
    # --------------------------------------

    embedding = (
        query_embedding_service.generate(
            query
        )
    )

    # --------------------------------------
    # Results
    # --------------------------------------

    print("\n==============================")
    print("QUERY EMBEDDING TEST")
    print("==============================")

    print("\nQuery:")
    print(query)

    print("\nEmbedding dimension:")
    print(len(embedding))

    print("\nEmbedding type:")
    print(type(embedding))

    print("\nFirst 10 values:")
    print(embedding[:10])

    print("\nIs empty:")
    print(len(embedding) == 0)

    print("\nSUCCESS")