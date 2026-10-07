import os
from openai import AsyncOpenAI
from config import LLM_PROVIDER

def configure_llm_client():
    """Configure the LLM client based on the selected provider and model."""
    if LLM_PROVIDER == "openrouter":
        return AsyncOpenAI(
            api_key=os.getenv("OPENROUTER_API_KEY"),
            base_url="https://openrouter.ai/api/v1",
        )
    elif LLM_PROVIDER == "ollama":
        return AsyncOpenAI(
            base_url="http://localhost:11434/v1",
            api_key="ollama"
        )
    elif LLM_PROVIDER == "openai":
        return AsyncOpenAI(
            api_key=os.getenv("OPENAI_API_KEY"),
        )
    else:
        raise ValueError(f"Unsupported LLM provider: {LLM_PROVIDER}")