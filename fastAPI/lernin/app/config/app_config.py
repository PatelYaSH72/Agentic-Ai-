from pydantic_settings import BaseSettings, SettingsConfigDict
from functools import lru_cache

class AppConfig(BaseSettings):
  app_name:str 
  app_env:str 
  database_url:str


  model_config = SettingsConfigDict(env_file=".env")

@lru_cache
def getAppConfig():
  return AppConfig() #type: ignore