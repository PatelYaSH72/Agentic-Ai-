from app.services.processing.chunking import (
    RecursiveChunker,
)

from app.services.processing.document_structure_chunker import (
    DocumentStructureChunker,
)

from app.services.processing.semantic_chunker import (
    SemanticTextChunker,
)


class ChunkingFactory:

    @staticmethod
    def get_chunker(
        strategy: str,
    ):

        strategy = strategy.lower()

        if strategy == "recursive":

            return RecursiveChunker()

        if strategy == "document_structure":

            return DocumentStructureChunker()

        if strategy == "semantic":

            return SemanticTextChunker()

        raise ValueError(
            f"Unsupported chunking strategy: {strategy}"
        )