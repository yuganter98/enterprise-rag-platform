from langchain_openai import ChatOpenAI
from langchain_core.language_models import LLM
from app.core.config import settings

def get_llm() -> LLM:
    """
    Returns the LLM instance to be used for RAG.
    configured for Local LLM (LM Studio / Ollama) via OpenAI-compatible API.
    """
    return ChatOpenAI(
        base_url=settings.LLM_BASE_URL,
        api_key=settings.LLM_API_KEY,
        temperature=0.7,
        model="local-model"  # Name doesn't matter for LM Studio usually
    )
