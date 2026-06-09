from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from typing import Annotated
from fastapi import Depends, HTTPException, status
from .helper import decodeAccessToken
from jwt.exceptions import InvalidTokenError

oauth2_schema = OAuth2PasswordBearer(tokenUrl="api/auth/login")

def authenticate_user(token:Annotated[str, Depends(oauth2_schema)]):
  try:
    payload = decodeAccessToken(token)
    print(f"The payload is: {payload}")
    return payload
  except InvalidTokenError:
    raise HTTPException(
      status_code=status.HTTP_401_UNAUTHORIZED,
      detail="Unauthorized",
      headers={"Authorization":"Bearer"}
    )