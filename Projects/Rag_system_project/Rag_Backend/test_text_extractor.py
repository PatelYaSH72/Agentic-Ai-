from app.core.database import SessionLocal

from app.services.retrieval.hybrid_search import (
    HybridSearchService,
)


def test_hybrid_search():

    db = SessionLocal()

    try:

        query = "database"

        print("\n==============================")
        print("HYBRID SEARCH TEST")
        print("==============================")

        print("\nQuery:")
        print(query)

        service = HybridSearchService(db)

        results = service.search(
            query=query,
            limit=5,
            document_id=1,
        )

        vector_results = (
            results["vector_results"]
        )

        keyword_results = (
            results["keyword_results"]
        )

        print("\n==============================")
        print("VECTOR RESULTS")
        print("==============================")

        print(
            "Results found:",
            len(vector_results),
        )

        for result in vector_results:

            print("\n------------------------------")

            print("Chunk ID:", result.id)

            print(
                "Chunk Index:",
                result.chunk_index,
            )

            print(
                "Text:",
                result.chunk_text[:200],
            )

        print("\n==============================")
        print("KEYWORD RESULTS")
        print("==============================")

        print(
            "Results found:",
            len(keyword_results),
        )

        for result in keyword_results:

            print("\n------------------------------")

            print("Chunk ID:", result.id)

            print(
                "Chunk Index:",
                result.chunk_index,
            )

            print(
                "Text:",
                result.chunk_text[:200],
            )

        print("\n==============================")
        print("HYBRID SEARCH SUCCESS")
        print("==============================")

    finally:

        db.close()


if __name__ == "__main__":

    test_hybrid_search()