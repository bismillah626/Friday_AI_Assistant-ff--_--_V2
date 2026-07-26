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


@st.cache_resource(show_spinner="Initializing memory…")
def load_memory_manager():
    """Return a MemoryManager instance. Cached — created once."""
    return MemoryManager()


@st.cache_resource(show_spinner="Creating agents…")
def load_agents(_flash_llm, _pro_llm, _memory_manager):
    """Build flash + pro agents. Underscored args tell Streamlit not to hash them."""
    flash_agent = create_friday_agent(_flash_llm, _memory_manager.conversational_memory)
    pro_agent = create_friday_agent(_pro_llm, _memory_manager.conversational_memory)
    return flash_agent, pro_agent
