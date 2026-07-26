"""All custom CSS / theme injection lives here — nowhere else."""

import streamlit as st

CUSTOM_CSS = """
<style>
/* ── Import Google Font ─────────────────────────── */
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');

/* ── Root variables ─────────────────────────────── */
:root {
    --bg-primary: #0a0a0f;
    --bg-secondary: #12121a;
    --bg-card: #1a1a2e;
    --accent: #7c3aed;
    --accent-glow: rgba(124, 58, 237, 0.35);
    --accent-light: #a78bfa;
    --text-primary: #e8e8f0;
    --text-secondary: #8888a0;
    --user-bubble: #7c3aed;
    --assistant-bubble: #1e1e30;
    --border-subtle: rgba(255, 255, 255, 0.06);
    --radius: 16px;
}

/* ── Global resets ──────────────────────────────── */
html, body, [data-testid="stAppViewContainer"],
[data-testid="stApp"] {
    background-color: var(--bg-primary) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Hide Streamlit chrome ──────────────────────── */
#MainMenu, header, footer,
[data-testid="stToolbar"],
[data-testid="stDecoration"],
.stDeployButton {
    display: none !important;
}

/* ── Sidebar ────────────────────────────────────── */
[data-testid="stSidebar"] {
    background: var(--bg-secondary) !important;
    border-right: 1px solid var(--border-subtle) !important;
}
[data-testid="stSidebar"] * {
    color: var(--text-primary) !important;
}

/* ── Chat input ─────────────────────────────────── */
[data-testid="stChatInput"] {
    background: var(--bg-secondary) !important;
    border-top: 1px solid var(--border-subtle) !important;
}
[data-testid="stChatInput"] textarea {
    background: var(--bg-card) !important;
    color: var(--text-primary) !important;
    border: 1px solid var(--border-subtle) !important;
    border-radius: 12px !important;
    font-family: 'Inter', sans-serif !important;
    transition: border-color 0.3s, box-shadow 0.3s;
}
[data-testid="stChatInput"] textarea:focus {
    border-color: var(--accent) !important;
    box-shadow: 0 0 20px var(--accent-glow) !important;
    outline: none !important;
}

/* ── Chat message bubbles ───────────────────────── */
[data-testid="stChatMessage"] {
    background: transparent !important;
    border: none !important;
    padding: 0.5rem 1rem !important;
}
/* user bubble */
[data-testid="stChatMessage"][data-testid-type="user"] .stMarkdown {
    background: var(--user-bubble);
    color: #fff;
    border-radius: var(--radius) var(--radius) 4px var(--radius);
    padding: 12px 18px;
    max-width: 80%;
    margin-left: auto;
}
/* assistant bubble */
[data-testid="stChatMessage"][data-testid-type="assistant"] .stMarkdown {
    background: var(--assistant-bubble);
    border: 1px solid var(--border-subtle);
    border-radius: var(--radius) var(--radius) var(--radius) 4px;
    padding: 12px 18px;
    max-width: 85%;
    color: var(--text-primary);
}

/* ── Avatar icons ───────────────────────────────── */
[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-user"] {
    background: var(--accent) !important;
}
[data-testid="stChatMessage"] [data-testid="chatAvatarIcon-assistant"] {
    background: linear-gradient(135deg, #7c3aed, #06b6d4) !important;
}

/* ── Custom scrollbar ───────────────────────────── */
::-webkit-scrollbar {
    width: 6px;
}
::-webkit-scrollbar-track {
    background: var(--bg-primary);
}
::-webkit-scrollbar-thumb {
    background: var(--accent);
    border-radius: 3px;
}
::-webkit-scrollbar-thumb:hover {
    background: var(--accent-light);
}

/* ── Buttons ────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent), #06b6d4) !important;
    color: #fff !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: 600 !important;
    font-family: 'Inter', sans-serif !important;
    padding: 0.55rem 1.2rem !important;
    transition: transform 0.15s, box-shadow 0.3s !important;
}
.stButton > button:hover {
    transform: translateY(-1px) !important;
    box-shadow: 0 4px 20px var(--accent-glow) !important;
}

/* ── Model badge ────────────────────────────────── */
.model-badge {
    display: inline-block;
    padding: 6px 14px;
    border-radius: 20px;
    font-size: 0.8rem;
    font-weight: 600;
    letter-spacing: 0.03em;
    margin-top: 6px;
}
.badge-flash {
    background: rgba(250, 204, 21, 0.12);
    color: #facc15;
    border: 1px solid rgba(250, 204, 21, 0.25);
}
.badge-pro {
    background: rgba(124, 58, 237, 0.12);
    color: var(--accent-light);
    border: 1px solid rgba(124, 58, 237, 0.25);
}

/* ── Thinking indicator ─────────────────────────── */
@keyframes pulse-dot {
    0%, 80%, 100% { opacity: 0.3; transform: scale(0.8); }
    40% { opacity: 1; transform: scale(1.1); }
}
.thinking-dot {
    display: inline-block;
    width: 8px; height: 8px;
    border-radius: 50%;
    background: var(--accent-light);
    margin: 0 3px;
    animation: pulse-dot 1.4s infinite ease-in-out;
}
.thinking-dot:nth-child(2) { animation-delay: 0.2s; }
.thinking-dot:nth-child(3) { animation-delay: 0.4s; }

/* ── Starter chip buttons ───────────────────────── */
.starter-chip {
    display: inline-block;
    background: var(--bg-card);
    border: 1px solid var(--border-subtle);
    border-radius: 24px;
    padding: 10px 20px;
    margin: 6px;
    color: var(--text-secondary);
    font-size: 0.85rem;
    cursor: pointer;
    transition: all 0.2s;
}
.starter-chip:hover {
    border-color: var(--accent);
    color: var(--text-primary);
    background: rgba(124, 58, 237, 0.08);
    box-shadow: 0 0 12px var(--accent-glow);
}

/* ── Animated gradient on input area ────────────── */
@keyframes gradient-shift {
    0% { background-position: 0% 50%; }
    50% { background-position: 100% 50%; }
    100% { background-position: 0% 50%; }
}
[data-testid="stChatInput"]::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--accent), #06b6d4, transparent);
    background-size: 200% 100%;
    animation: gradient-shift 3s linear infinite;
}

/* ── Sidebar title glow ─────────────────────────── */
.sidebar-title {
    font-size: 1.6rem;
    font-weight: 700;
    background: linear-gradient(135deg, #7c3aed, #06b6d4);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.2rem;
}
.sidebar-subtitle {
    font-size: 0.78rem;
    color: var(--text-secondary);
    margin-bottom: 1.5rem;
}
</style>
"""


def inject_css():
    """Inject the full custom CSS once per page load."""
    st.markdown(CUSTOM_CSS, unsafe_allow_html=True)
