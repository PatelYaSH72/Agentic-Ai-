from langchain_experimental.text_splitter import (
    SemanticChunker,
)

from langchain_community.embeddings import (
    HuggingFaceEmbeddings,
)


class SemanticTextChunker:

    def __init__(self):

        embeddings = HuggingFaceEmbeddings(
            model_name="BAAI/bge-small-en-v1.5",
        )

        self.chunker = SemanticChunker(
            embeddings,
        )

    def split_text(
        self,
        text: str,
    ) -> list[str]:

        documents = self.chunker.create_documents(
            [text],
        )

        return [
            document.page_content
            for document in documents
        ]