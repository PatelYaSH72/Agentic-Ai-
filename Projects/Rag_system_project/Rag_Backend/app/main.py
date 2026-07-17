from fastapi import FastAPI

app = FastAPI(
    title="Enterprise RAG Studio"
)

@app.get("/")
def root():
    return {
        "message":"Enterprise RAG Studio API"
    }