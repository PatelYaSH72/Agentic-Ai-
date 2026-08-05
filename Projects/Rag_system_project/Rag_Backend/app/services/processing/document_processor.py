from app.services.processing.text_extractor import (
    TextExtractor,
)

from app.services.processing.chunking_factory import (
    ChunkingFactory,
)


class DocumentProcessor:

    def __init__(self):

        self.extractor = TextExtractor()

    def process_document(
        self,
        file_path: str,
        chunking_strategy: str,
    ) -> list[str]:

        # -------------------------------
        # Extract text
        # -------------------------------

        text = self.extractor.extract_text(
            file_path
        )

        # -------------------------------
        # Select chunker
        # -------------------------------

        chunker = ChunkingFactory.get_chunker(
            chunking_strategy
        )

        # -------------------------------
        # Generate chunks
        # -------------------------------

        chunks = chunker.split_text(
            text
        )

        return chunks