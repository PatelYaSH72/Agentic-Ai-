from pydantic import BaseModel, Field


class RetrievalRequest(BaseModel):

    query: str = Field(
        ...,
        min_length=1,
        description="User search query",
    )

    limit: int = Field(
        default=5,
        ge=1,
        le=20,
        description="Number of chunks to retrieve",
    )

    document_id: int | None = Field(
        default=None,
    )

    collection_id: int | None = Field(
        default=None,
    )

class RetrievalResult(BaseModel):

    chunk_id: int
    document_id: int
    chunk_index: int
    chunk_text: str
    page_number: int | None
    chunk_size: int
    chunking_strategy: str


class RetrievalResponse(BaseModel):

    query: str
    results: list[RetrievalResult]
    result_count: int