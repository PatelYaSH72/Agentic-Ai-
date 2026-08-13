class RRFService:

    def __init__(self, k: int = 60):
        self.k = k

    def combine(
        self,
        vector_results,
        keyword_results,
        limit: int = 5,
    ):
        scores = {}
        result_map = {}

        # --------------------------------------
        # Vector Search Ranking
        # --------------------------------------

        for rank, result in enumerate(vector_results, start=1):

            result_id = result.id

            scores[result_id] = (
                scores.get(result_id, 0)
                + 1 / (self.k + rank)
            )

            result_map[result_id] = result

        # --------------------------------------
        # Keyword Search Ranking
        # --------------------------------------

        for rank, result in enumerate(
            keyword_results,
            start=1,
        ):

            result_id = result.id

            scores[result_id] = (
                scores.get(result_id, 0)
                + 1 / (self.k + rank)
            )

            result_map[result_id] = result

        # --------------------------------------
        # Sort by RRF score
        # --------------------------------------

        ranked_ids = sorted(
            scores,
            key=scores.get,
            reverse=True,
        )

        # --------------------------------------
        # Return Top-K
        # --------------------------------------

        return [
            result_map[result_id]
            for result_id in ranked_ids[:limit]
        ]