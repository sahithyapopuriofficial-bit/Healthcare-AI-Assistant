"""
Healthcare AI Assistant — Streamlit application entrypoint.
"""

import streamlit as st

from config.settings import settings
from ui.chat_interface import render_chat_interface
from ui.sidebar import render_sidebar
from ui.styles import DARK_THEME_CSS


def main() -> None:
    """Configure the page, apply styling, and render the app layout."""
    st.set_page_config(
        page_title=settings.app_name,
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.markdown(DARK_THEME_CSS, unsafe_allow_html=True)

    if "messages" not in st.session_state:
        st.session_state["messages"] = []

    render_sidebar()

    st.markdown(
        f"""
        <div class="hc-header">
            <div style="font-size:2rem;">🩺</div>
            <div>
                <p class="hc-title">{settings.app_name}</p>
                <p class="hc-tagline">{settings.app_tagline}</p>
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    if not settings.groq_api_key:
        st.error(
            "⚠️ GROQ_API_KEY is not configured. Add it to your .env file "
            "(or Streamlit Cloud Secrets) before chatting."
        )

    render_chat_interface()

    st.markdown(
        f'<div class="hc-footer">{settings.disclaimer}</div>',
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    main()
