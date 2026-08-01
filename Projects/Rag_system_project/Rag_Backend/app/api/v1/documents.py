from pathlib import Path
from uuid import uuid4

from fastapi import (
    APIRouter,
    Depends,
    File,
    UploadFile,
    HTTPException,
    status,
)

from sqlalchemy.orm import Session

from app.api.dependencies import get_current_user
from app.core.database import get_db

from app.models.user import User
from app.models.document import Document
from app.models.collection import Collection


router = APIRouter(
    prefix="/documents",
    tags=["Knowledge Base"],
)


# ==========================================
# UPLOAD DIRECTORY
# ==========================================

UPLOAD_DIR = Path("uploads/documents")

UPLOAD_DIR.mkdir(
    parents=True,
    exist_ok=True,
)


# ==========================================
# ALLOWED FILE TYPES
# ==========================================

ALLOWED_EXTENSIONS = {
    ".pdf",
    ".docx",
    ".txt",
    ".md",
}


# ==========================================
# UPLOAD DOCUMENT
# ==========================================

@router.post(
    "/upload",
    status_code=status.HTTP_201_CREATED,
)
def upload_document(
    collection_id: int,
    file: UploadFile = File(...),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Upload a document and save its metadata.
    """

    # --------------------------------------
    # Validate filename
    # --------------------------------------

    if not file.filename:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="File name is required",
        )

    # --------------------------------------
    # Validate extension
    # --------------------------------------

    file_extension = Path(
        file.filename
    ).suffix.lower()

    if file_extension not in ALLOWED_EXTENSIONS:

        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                "Unsupported file type. "
                f"Allowed types: "
                f"{', '.join(ALLOWED_EXTENSIONS)}"
            ),
        )

    # --------------------------------------
    # Check collection
    # --------------------------------------

    collection = (
        db.query(Collection)
        .filter(
            Collection.id == collection_id,
            Collection.created_by == current_user.id,
        )
        .first()
    )

    if not collection:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Collection not found",
        )

    # --------------------------------------
    # Generate unique filename
    # --------------------------------------

    stored_filename = (
        f"{uuid4().hex}"
        f"{file_extension}"
    )

    file_path = (
        UPLOAD_DIR
        / stored_filename
    )

    # --------------------------------------
    # Save file
    # --------------------------------------

    file_content = file.file.read()

    with open(
        file_path,
        "wb",
    ) as buffer:

        buffer.write(
            file_content
        )

    # --------------------------------------
    # Create database record
    # --------------------------------------

    document = Document(

        title=Path(
            file.filename
        ).stem,

        original_filename=file.filename,

        stored_filename=stored_filename,

        file_type=file_extension,

        file_size=len(file_content),

        file_path=str(file_path),

        collection_id=collection.id,

        uploaded_by=current_user.id,

        is_processed=False,

        processing_status="pending",
    )

    db.add(document)

    db.commit()

    db.refresh(document)

    # --------------------------------------
    # Response
    # --------------------------------------

    return {

        "message": "Document uploaded successfully",

        "document_id": document.id,

        "title": document.title,

        "original_filename": document.original_filename,

        "stored_filename": document.stored_filename,

        "file_size": document.file_size,

        "file_type": document.file_type,

        "collection_id": document.collection_id,

        "collection_name": collection.name,

        "uploaded_by": document.uploaded_by,

        "processing_status": document.processing_status,
    }


@router.get("/")
def get_documents(
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):

    documents = (
        db.query(Document)
        .filter(
            Document.uploaded_by == current_user.id
        )
        .order_by(
            Document.created_at.desc()
        )
        .all()
    )

    return {
        "total": len(documents),
        "documents": [
            {
                "id": document.id,
                "title": document.title,
                "original_filename": document.original_filename,
                "file_type": document.file_type,
                "file_size": document.file_size,
                "collection_id": document.collection_id,
                "processing_status": document.processing_status,
                "created_at": document.created_at,
            }
            for document in documents
        ],
    }


# ==========================================
# GET SINGLE DOCUMENT
# ==========================================

@router.get(
    "/{document_id}",
)
def get_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Get a single document by ID.
    """

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.uploaded_by == current_user.id,
        )
        .first()
    )

    if not document:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    return {

        "id": document.id,

        "title": document.title,

        "original_filename": document.original_filename,

        "stored_filename": document.stored_filename,

        "file_type": document.file_type,

        "file_size": document.file_size,

        "file_path": document.file_path,

        "collection_id": document.collection_id,

        "uploaded_by": document.uploaded_by,

        "is_processed": document.is_processed,

        "processing_status": document.processing_status,

        "total_pages": document.total_pages,

        "total_chunks": document.total_chunks,

        "embedding_model": document.embedding_model,

        "created_at": document.created_at,

        "updated_at": document.updated_at,
    }


# ==========================================
# DELETE DOCUMENT
# ==========================================

@router.delete(
    "/{document_id}",
    status_code=status.HTTP_200_OK,
)
def delete_document(
    document_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Delete a document.
    """

    document = (
        db.query(Document)
        .filter(
            Document.id == document_id,
            Document.uploaded_by == current_user.id,
        )
        .first()
    )

    if not document:

        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Document not found",
        )

    # --------------------------------------
    # Delete physical file
    # --------------------------------------

    file_path = Path(document.file_path)

    if file_path.exists():

        file_path.unlink()

    # --------------------------------------
    # Delete database record
    # --------------------------------------

    db.delete(document)

    db.commit()

    # --------------------------------------
    # Response
    # --------------------------------------

    return {
        "message": "Document deleted successfully",
        "document_id": document_id,
    }



