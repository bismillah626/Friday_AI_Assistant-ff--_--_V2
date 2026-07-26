"""Friday AI — Streamlit frontend entry point."""

import streamlit as st
from ui.styles import inject_css
from ui.state import init_state

# ── Page config (must be first st call) ─────────
st.set_page_config(
    page_title="Friday AI",
    page_icon="🤖",
    layout="centered",
    initial_sidebar_state="expanded",
)

# ── Inject theme + init state ───────────────────
inject_css()
init_state()

# ── Sidebar ─────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">🤖 Friday AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Your intelligent assistant</div>', unsafe_allow_html=True)

# ── Placeholder for chat loop ───────────────────
st.markdown("### Chat coming soon…")
