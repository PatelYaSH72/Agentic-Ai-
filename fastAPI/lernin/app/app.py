from fastapi import FastAPI , Depends
from typing import Annotated
from app.routing import todo, auth
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
from app.config.app_config import getAppConfig

app = FastAPI()

# Include all routes
app.include_router(todo.router, prefix="/api")
app.include_router(auth.router, prefix="/api")

@app.exception_handler(RequestValidationError)
async def validation_exceprion_handler(request, exc): 
     errors = {}
     for error in exc.errors():
          print(f"The error is: {error}")
          errors[error['loc'][-1]] = error["msg"]

     return JSONResponse({"message":"Validation Error", "error":errors},status_code=422)

@app.get("/")
def root():
    config = getAppConfig()
    return {"message":f"Hello, world! ",
             "app_name":config.app_name,
              "app_env": config.app_env,
              "app_env": config.app_env,
              "database_url":config.database_url
             }