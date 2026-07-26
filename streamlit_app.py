"""Friday AI — Streamlit frontend entry point."""

import streamlit as st
from ui.styles import inject_css
from ui.state import init_state, append_message
from ui.loader import load_llms, load_memory_manager, load_agents
from ui.router import route_query
from ui.context import build_agent_input, save_interaction
from ui.chat import render_message, stream_response, show_thinking_indicator

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

# ── Load cached resources ───────────────────────
flash_llm, pro_llm = load_llms()
memory_manager = load_memory_manager()
flash_agent, pro_agent = load_agents(flash_llm, pro_llm, memory_manager)

# ── Sidebar ─────────────────────────────────────
with st.sidebar:
    st.markdown('<div class="sidebar-title">🤖 Friday AI</div>', unsafe_allow_html=True)
    st.markdown('<div class="sidebar-subtitle">Your intelligent assistant</div>', unsafe_allow_html=True)

# ── Render existing chat history ────────────────
for msg in st.session_state.messages:
    render_message(msg["role"], msg["content"])

# ── Empty-state hero (when no messages yet) ─────
STARTER_PROMPTS = [
    "What's the weather like?",
    "Tell me a joke",
    "Explain quantum computing",
    "Play some music on Spotify",
    "What can you do?",
]

if not st.session_state.messages:
    st.markdown(
        '<div class="empty-hero">'
        '<span class="empty-hero-icon">🤖</span>'
        '<div class="empty-hero-title">Hey Boss, I\'m Friday</div>'
        '<div class="empty-hero-sub">Your AI assistant — ask me anything to get started</div>'
        "</div>",
        unsafe_allow_html=True,
    )
    # clickable starter chips
    cols = st.columns(len(STARTER_PROMPTS))
    for i, prompt in enumerate(STARTER_PROMPTS):
        with cols[i]:
            if st.button(prompt, key=f"starter_{i}", use_container_width=True):
                st.session_state["_prefill"] = prompt
                st.rerun()

# ── Check for prefill from starter chip ─────────
prefill = st.session_state.pop("_prefill", None)

# ── Chat input ──────────────────────────────────
user_input = prefill or st.chat_input("Ask Friday anything…")

if user_input:
    # show user message immediately
    append_message("user", user_input)
    render_message("user", user_input)

    # show thinking indicator while agent works
    thinking = show_thinking_indicator()

    # route to correct model
    chosen = route_query(user_input, flash_llm)
    active_agent = pro_agent if chosen == "powerful" else flash_agent
    st.session_state.last_model = chosen

    # build context-enriched input and get response
    agent_input = build_agent_input(user_input, memory_manager)
    response = active_agent.invoke({"input": agent_input})
    response_text = response["output"]

    # clear thinking indicator
    thinking.empty()

    # stream the response
    stream_response(response_text)
    append_message("assistant", response_text)

    # persist to memory
    save_interaction(user_input, response_text, memory_manager)
