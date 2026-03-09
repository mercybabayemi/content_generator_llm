from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_KEY: str = "ollama"
    MODEL_NAME: str = "qwen2.5:3b"
    BASE_URL: str = "http://localhost:11434/v1"

settings = Settings()
