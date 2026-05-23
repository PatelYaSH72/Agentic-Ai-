from fastapi import FastAPI
from database import engine, Base
from routes.user import router

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Auth System")
app.include_router(router)

@app.get("/")
def root():
    return {"message": "Auth API running"}