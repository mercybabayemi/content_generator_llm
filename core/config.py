from pydantic_settings import BaseSettings
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    api_key: str = os.getenv("API_KEY")
    model_name: str = os.getenv("MODEL_NAME")
    ollama_base_url: str = os.getenv("OLLAMA_BASE_URL")

settings = Settings()
