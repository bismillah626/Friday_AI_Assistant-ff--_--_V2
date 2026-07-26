"""Chat rendering: message display and streaming."""

import time
import streamlit as st


def render_message(role: str, content: str):
    """Display a single chat message using Streamlit's native chat_message."""
    with st.chat_message(role):
        st.markdown(content)


def stream_response(response_text: str):
    """Simulate token-by-token streaming inside an assistant chat bubble."""
    with st.chat_message("assistant"):
        placeholder = st.empty()
        streamed = ""
        words = response_text.split(" ")
        for i, word in enumerate(words):
            streamed += word + (" " if i < len(words) - 1 else "")
            placeholder.markdown(streamed + "▌")
            time.sleep(0.03)
        # final render without cursor
        placeholder.markdown(streamed)
    return streamed


def show_thinking():
    """Display a pulsing 'thinking…' indicator inside an assistant bubble."""
    thinking_html = (
        '<div style="display:flex;align-items:center;gap:6px;">'
        '<span class="thinking-dot"></span>'
        '<span class="thinking-dot"></span>'
        '<span class="thinking-dot"></span>'
        '<span style="color:#8888a0;font-size:0.85rem;margin-left:4px;">'
        "Friday is thinking…</span></div>"
    )
    return st.chat_message("assistant").empty(), thinking_html
