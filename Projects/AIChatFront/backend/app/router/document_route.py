from fastapi import APIRouter

from app.schema.document_schema import DocumentRequest, UserQuery
from app.services.document_services import rag_chunk, user_query

rag_chunkrouter = APIRouter(prefix="/documents",  tags=["Documents"])

@rag_chunkrouter.post("/ingect")
async def ingect_document(payload: DocumentRequest):
  return await rag_chunk(payload.content)

@rag_chunkrouter.post("/get-data")
async def get_Data(query:UserQuery):
  return await user_query(query.query)