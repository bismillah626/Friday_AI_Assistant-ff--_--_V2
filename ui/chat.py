"""Chat rendering: message display and streaming."""

import streamlit as st


def render_message(role: str, content: str):
    """Display a single chat message using Streamlit's native chat_message."""
    with st.chat_message(role):
        st.markdown(content)
