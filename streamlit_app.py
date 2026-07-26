"""Friday AI — Streamlit frontend entry point."""

import streamlit as st
from ui.styles import inject_css
from ui.state import init_state, append_message, clear_history
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

    if st.button("✨ New Chat", key="new_chat", use_container_width=True):
        clear_history()
        st.rerun()

    st.markdown('<div class="sidebar-divider"></div>', unsafe_allow_html=True)

    # model badge
    st.markdown('<div class="sidebar-label">Last model used</div>', unsafe_allow_html=True)
    model = st.session_state.last_model
    if model == "powerful":
        st.markdown(
            '<span class="model-badge badge-pro">🧠 Gemini Pro</span>',
            unsafe_allow_html=True,
        )
    elif model == "standard":
        st.markdown(
            '<span class="model-badge badge-flash">⚡ Gemini Flash</span>',
            unsafe_allow_html=True,
        )
    else:
        st.markdown(
            '<span style="color:#8888a0;font-size:0.8rem;">No queries yet</span>',
            unsafe_allow_html=True,
        )

# ── Render existing chat history ────────────────
for msg in st.session_state.messages:
    render_message(msg["role"], msg["content"])

# ── Empty-state hero (when no messages yet) ─────
STARTER_PROMPTS = [
    "🌤️ What's the weather like?",
    "😂 Tell me a joke",
    "🔬 Explain quantum computing",
    "🎵 Play some music",
    "💡 What can you do?",
    "🐍 Help me with Python",
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
    # clickable starter chips — 3 per row
    row1 = st.columns(3)
    row2 = st.columns(3)
    for i, prompt in enumerate(STARTER_PROMPTS[:3]):
        with row1[i]:
            if st.button(prompt, key=f"starter_{i}", use_container_width=True):
                st.session_state["_prefill"] = prompt
                st.rerun()
    for i, prompt in enumerate(STARTER_PROMPTS[3:]):
        with row2[i]:
            if st.button(prompt, key=f"starter_{i+3}", use_container_width=True):
                st.session_state["_prefill"] = prompt
                st.rerun()

# ── Check for prefill from starter chip ─────────
prefill = st.session_state.pop("_prefill", None)

# ── Chat input ──────────────────────────────────
user_input = prefill or st.chat_input("Ask Friday anything…")

if user_input:
    # strip emoji prefix from starter chips if present
    clean_input = user_input.split(" ", 1)[-1] if user_input[0] not in "abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ" and " " in user_input else user_input

    # show user message immediately
    append_message("user", clean_input)
    render_message("user", clean_input)

    # show thinking indicator while agent works
    thinking = show_thinking_indicator()

    try:
        # route to correct model
        chosen = route_query(clean_input, flash_llm)
        active_agent = pro_agent if chosen == "powerful" else flash_agent
        st.session_state.last_model = chosen

        # build context-enriched input and get response
        agent_input = build_agent_input(clean_input, memory_manager)
        response = active_agent.invoke({"input": agent_input})
        response_text = response["output"]

        # clear thinking indicator
        thinking.empty()

        # stream the response
        stream_response(response_text)
        append_message("assistant", response_text)

        # persist to memory
        save_interaction(clean_input, response_text, memory_manager)

    except Exception as e:
        thinking.empty()
        error_msg = f"Sorry, something went wrong: {e}"
        render_message("assistant", error_msg)
        append_message("assistant", error_msg)
