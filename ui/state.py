"""Session state initialization and chat history helpers."""

import streamlit as st


def init_state():
    """Set up default session_state keys if they don't exist yet."""
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "last_model" not in st.session_state:
        st.session_state.last_model = None


def append_message(role: str, content: str):
    """Add a message dict to the chat history."""
    st.session_state.messages.append({"role": role, "content": content})


def clear_history():
    """Wipe chat history and reset model badge."""
    st.session_state.messages = []
    st.session_state.last_model = None
