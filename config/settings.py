"""
Application-wide configuration and environment variable loading.

Reads from Streamlit Cloud's `st.secrets` first (used when deployed), falling
back to OS environment variables / a local `.env` file (used when running
locally). This means the same code works in both environments without
changes.
"""

import os
from dataclasses import dataclass

from dotenv import load_dotenv

load_dotenv()


def _get_setting(key: str, default: str = "") -> str:
    """Fetch a config value, preferring Streamlit secrets over env vars.

    Args:
        key: The setting name (e.g. 'GROK_API_KEY').
        default: Value to return if not found anywhere.

    Returns:
        str: The resolved setting value.
    """
    try:
        import streamlit as st

        if key in st.secrets:
            return str(st.secrets[key])
    except Exception:
        # st.secrets raises if no secrets.toml exists (e.g. local runs
        # without Streamlit Cloud secrets configured) — fall through to env.
        pass

    return os.getenv(key, default)


@dataclass(frozen=True)
class Settings:
    """Immutable application settings loaded from Streamlit secrets or environment variables."""

    groq_api_key: str = _get_setting("GROQ_API_KEY")
    groq_api_base: str = _get_setting("GROQ_API_BASE", "https://api.groq.com/openai/v1")
    groq_model_name: str = _get_setting("GROQ_MODEL_NAME", "llama-3.3-70b-versatile")

    langchain_api_key: str = _get_setting("LANGCHAIN_API_KEY")
    langchain_project: str = _get_setting("LANGCHAIN_PROJECT", "healthcare-ai-assistant")
    langchain_tracing_v2: bool = _get_setting("LANGCHAIN_TRACING_V2", "false").lower() == "true"

    app_name: str = "Healthcare AI Assistant"
    app_tagline: str = "Your Trusted AI Companion for Health Education"

    temperature: float = 0.3
    max_tokens: int = 2048
    streaming: bool = True

    disclaimer: str = (
        "This AI assistant provides educational information only and "
        "should not replace professional medical advice."
    )


def configure_langsmith(settings: "Settings") -> None:
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
