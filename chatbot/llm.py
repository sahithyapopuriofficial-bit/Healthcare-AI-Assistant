"""
LLM initialization for Grok AI (xAI API) using an OpenAI-compatible client.

xAI's Grok API is OpenAI-compatible, so we use langchain_openai's ChatOpenAI
pointed at the xAI base URL.
"""

from langchain_openai import ChatOpenAI

from config.settings import settings


def get_llm() -> ChatOpenAI:
    """Create and return a configured Grok (xAI) chat model instance.

    Returns:
        ChatOpenAI: A LangChain chat model wired to the xAI Grok endpoint.

    Raises:
        ValueError: If no API key is configured.
    """
    if not settings.grok_api_key:
        raise ValueError(
            "GROK_API_KEY is not set. Please add it to your .env file."
        )

    return ChatOpenAI(
        model=settings.grok_model_name,
        api_key=settings.grok_api_key,
        base_url=settings.grok_api_base,
        temperature=settings.temperature,
        max_tokens=settings.max_tokens,
        streaming=settings.streaming,
    )
