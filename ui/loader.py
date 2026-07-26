"""Cached loading: LLMs, MemoryManager, agents — loaded once per session."""

import streamlit as st
from core.llm_engine import get_flash_llm, get_pro_llm
from memory.memory_manager import MemoryManager
from agents.friday_agent import create_friday_agent


@st.cache_resource(show_spinner="Loading LLM models…")
def load_llms():
    """Return (flash_llm, pro_llm). Cached so models load exactly once."""
    flash = get_flash_llm()
    pro = get_pro_llm()
    return flash, pro
