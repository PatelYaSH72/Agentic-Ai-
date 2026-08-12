from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
)

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.schemas.retrieval import (
    RetrievalRequest,
    RetrievalResponse,
    RetrievalResult,
)

from app.services.retrieval.retrieval_service import (
    RetrievalService,
)


router = APIRouter(
    prefix="/retrieval",
    tags=["Retrieval"],
)


@router.post(
    "/search",
    response_model=RetrievalResponse,
)
def retrieve_documents(
    request: RetrievalRequest,
    db: Session = Depends(get_db),
):

    try:

        retrieval_service = (
            RetrievalService(db)
        )

        results = (
            retrieval_service.retrieve(
                query=request.query,
                limit=request.limit,
                document_id=request.document_id,
                collection_id=request.collection_id,
            )
        )

        response_results = []

        for result in results:

            response_results.append(
                RetrievalResult(
                    chunk_id=result.id,
                    document_id=result.document_id,
                    chunk_index=result.chunk_index,
                    chunk_text=result.chunk_text,
                    page_number=result.page_number,
                    chunk_size=result.chunk_size,
                    chunking_strategy=result.chunking_strategy,
                )
            )

        return RetrievalResponse(
            query=request.query,
            results=response_results,
            result_count=len(response_results),
        )

    except ValueError as exc:

        raise HTTPException(
            status_code=400,
            detail=str(exc),
        )

    except Exception as exc:

        raise HTTPException(
            status_code=500,
            detail=f"Retrieval failed: {str(exc)}",
        )