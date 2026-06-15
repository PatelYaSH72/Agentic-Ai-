from fastapi import FastAPI
from app.router import blog
from app.config.app_config import getAppConfig
from app.database.db import Base, engine

app = FastAPI()

app.include_router(blog.router, prefix="/api")

Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
  config = getAppConfig()
  return {
    "message":f"Hello, world! ",
             "app_name":config.app_name,
              "app_env": config.app_env,
              "app_env": config.app_env,
              "database_url":config.database_url
        }