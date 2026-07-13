"""
Application-wide configuration and environment variable loading.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


@dataclass(frozen=True)
class Settings:
    """Immutable application settings loaded from environment variables."""

    grok_api_key: str = os.getenv("GROK_API_KEY", "")
    grok_api_base: str = os.getenv("GROK_API_BASE", "https://api.x.ai/v1")
    grok_model_name: str = os.getenv("GROK_MODEL_NAME", "grok-2-latest")

    langchain_api_key: str = os.getenv("LANGCHAIN_API_KEY", "")
    langchain_project: str = os.getenv("LANGCHAIN_PROJECT", "healthcare-ai-assistant")
    langchain_tracing_v2: bool = os.getenv("LANGCHAIN_TRACING_V2", "false").lower() == "true"

    app_name: str = "Healthcare AI Assistant"
    app_tagline: str = "Your Trusted AI Companion for Health Education"

    temperature: float = 0.3
    max_tokens: int = 2048
    streaming: bool = True

    disclaimer: str = (
        "This AI assistant provides educational information only and "
        "should not replace professional medical advice."
    )


def configure_langsmith(settings: Settings) -> None:
    """Configure LangSmith tracing environment variables.

    Args:
        settings: Loaded application settings.
    """
    if settings.langchain_tracing_v2 and settings.langchain_api_key:
        os.environ["LANGCHAIN_TRACING_V2"] = "true"
        os.environ["LANGCHAIN_API_KEY"] = settings.langchain_api_key
        os.environ["LANGCHAIN_PROJECT"] = settings.langchain_project
    else:
        os.environ["LANGCHAIN_TRACING_V2"] = "false"


settings = Settings()
configure_langsmith(settings)
