from sentence_transformers import SentenceTransformer


class EmbeddingService:

    MODEL_NAME = "BAAI/bge-small-en-v1.5"

    EMBEDDING_DIMENSION = 384

    def __init__(self):

        self.model = SentenceTransformer(
            self.MODEL_NAME
        )

    def generate_embedding(
        self,
        text: str,
    ) -> list[float]:

        if not text or not text.strip():
            raise ValueError(
                "Text cannot be empty"
            )

        embedding = self.model.encode(
            text,
            normalize_embeddings=True,
        )

        return embedding.tolist()

    def generate_embeddings(
        self,
        texts: list[str],
    ) -> list[list[float]]:

        if not texts:
            return []

        embeddings = self.model.encode(
            texts,
            normalize_embeddings=True,
        )

        return embeddings.tolist()