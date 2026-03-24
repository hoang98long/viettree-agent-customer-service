from pydantic import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "Agentic AI"
    LLM_MODEL: str = "llama3"
    EMBEDDING_MODEL: str = "sentence-transformers/all-MiniLM-L6-v2"

settings = Settings()