from fastapi import (
    APIRouter,
    Depends,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db

from app.models.collection import Collection
from app.models.user import User

from app.schemas.collection import (
    CollectionCreate,
    CollectionResponse,
)


router = APIRouter(
    prefix="/collections",
    tags=["Collections"],
)


@router.post(
    "/",
    response_model=CollectionResponse,
    status_code=status.HTTP_201_CREATED,
)
def create_collection(
    collection_data: CollectionCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    existing_collection = (
        db.query(Collection)
        .filter(
            Collection.name
            == collection_data.name,
            Collection.created_by
            == current_user.id,
        )
        .first()
    )

    if existing_collection:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Collection already exists",
        )

    collection = Collection(
        name=collection_data.name,
        description=collection_data.description,
        created_by=current_user.id,
    )

    db.add(collection)
    db.commit()
    db.refresh(collection)

    return collection

@router.get("/")
def get_collections(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get all collections of the current user.
    """

    collections = (
        db.query(Collection)
        .filter(
            Collection.created_by == current_user.id
        )
        .order_by(
            Collection.created_at.desc()
        )
        .all()
    )

    return {
        "total": len(collections),
        "collections": [
            {
                "id": collection.id,
                "name": collection.name,
                "description": collection.description,
                "created_at": collection.created_at,
            }
            for collection in collections
        ],
    }


    




