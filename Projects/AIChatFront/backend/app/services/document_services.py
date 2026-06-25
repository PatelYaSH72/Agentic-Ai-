from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from sqlalchemy import select
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_groq import ChatGroq

from app.db.database import SessionLocal
from app.db.models import Page

embedding_model = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

llm = ChatGroq(
    model="llama-3.3-70b-versatile"
)


async def rag_chunk(content: str):

    # 1. Chunking
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=800,
        chunk_overlap=100
    )

    chunks = splitter.split_text(content)

    # 2. Embedding Model
    embedding_model = HuggingFaceEmbeddings(
        model_name="sentence-transformers/all-MiniLM-L6-v2"
    )

    # 3. DB Session
    db = SessionLocal()

    try:

        stored_chunks = 0

        # 4. Process each chunk
        for chunk in chunks:

            embedding = embedding_model.embed_query(chunk)

            page = Page(
                content=chunk,
                embedding=embedding
            )

            db.add(page)

            stored_chunks += 1

        db.commit()

        return {
            "message": "Document processed successfully",
            "total_chunks": stored_chunks
        }

    except Exception as e:

        db.rollback()

        raise Exception(str(e))

    finally:
        db.close()


async def user_query(query: str):
    

    db = SessionLocal()

    try:

        # Query embedding
        query_embedding = embedding_model.embed_query(query)

        # Top 3 similar chunks
        results = db.scalars(
            select(Page)
            .order_by(
                Page.embedding.cosine_distance(
                    query_embedding
                )
            )
            .limit(3)
        ).all()

        context = "\n\n".join(
            [item.content for item in results]
        )

        prompt = f"""
You are a helpful AI assistant.

Answer only from the provided context.

Question:
{query}

Context:
{context}

If answer is not present in context,
reply:
Answer not found in the provided documents.
"""

        messages = [
            SystemMessage(
                content="You are a helpful assistant."
            ),
            HumanMessage(content=prompt),
        ]

        response = llm.invoke(messages)

        return {
            "query": query,
            "retrieved_chunks": len(results),
            "answer": response.content
        }

    finally:
        db.close()
    