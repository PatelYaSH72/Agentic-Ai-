from app.services.processing.text_extractor import (
    TextExtractor,
)

from app.services.processing.chunking_factory import (
    ChunkingFactory,
)

extractor = TextExtractor()

text = extractor.extract_text(
    "uploads/documents/de524d6524fe4b0c898a93b9c83fbc0f.pdf"
)

strategy = "recursive"
# strategy = "document_structure"
# strategy = "semantic"

chunker = ChunkingFactory.get_chunker(
    strategy
)

chunks = chunker.split_text(
    text
)

print(
    f"Strategy : {strategy}"
)

print(
    f"Chunks : {len(chunks)}"
)

for index, chunk in enumerate(
    chunks,
    start=1,
):

    print("=" * 80)

    print(f"Chunk {index}")

    print("=" * 80)

    print(chunk)