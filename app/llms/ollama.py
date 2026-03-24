from langchain_community.llms import Ollama
from app.core.config import settings

def get_llm():
    return Ollama(
        model=settings.LLM_MODEL,
        temperature=0
    )