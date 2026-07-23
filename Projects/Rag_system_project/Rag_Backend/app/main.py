from fastapi import FastAPI

from app.api.router import api_router
from app.core.exception_handler import app_exception_handler
from app.core.exceptions import AppException

app = FastAPI(
    title="Enterprise RAG Studio",
    version="1.0.0",
)

app.add_exception_handler(
    AppException,
    app_exception_handler,
)

app.include_router(
    api_router,
   
)


@app.get("/")
def root():
    return {
        "message": "Enterprise RAG Studio API"
    }