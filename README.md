# Friday AI Assistant

## Overview

Friday AI is an intelligent, modular LLM-driven assistant built for natural, emotionally aware interaction and contextual reasoning. It supports both a **voice-activated terminal mode** and a **modern Streamlit chat UI**.

Built with LangChain as the core framework — enabling conversational chains, task orchestration, and dynamic API routing. Features multi-layered memory (short-term conversational buffer + long-term FAISS vector store) for continuity across sessions. Uses Gemini 2.5 Flash/Pro for language understanding and automatic model routing based on query complexity.

## Tech Stack

| Category | Technology |
|---|---|
| **Core Language** | Python |
| **AI Framework** | LangChain |
| **LLM Provider** | Google Gemini (2.5 Flash + Pro) |
| **Vector Database** | FAISS |
| **Embeddings** | HuggingFace (all-MiniLM-L6-v2) |
| **Frontend** | Streamlit |
| **Voice Recognition** | SpeechRecognition + gTTS |
| **APIs & Integrations** | Spotify API, Open-Meteo Weather API |
| **Environment Management** | python-dotenv |

## Features

- **Streamlit Chat UI** — Dark-themed, ChatGPT-style interface with streaming responses, thinking indicators, and starter prompts
- **Smart Model Routing** — Automatically selects Gemini Flash (fast) or Pro (powerful) based on query complexity
- **Voice Activation** — Terminal mode responds to the wake word **"Friday"** (optional)
- **Conversational Memory** — Short-term buffer + long-term FAISS vector store for contextual follow-ups
- **Tool-Based Architecture** — Modular tools (Spotify, Weather, App Opener, Website Opener) registered with LangChain
- **Music Control** — Play/pause tracks via the **Spotify API**
- **Weather Assistant** — Real-time weather data from the **Open-Meteo API**
- **Extensible** — Add your own tools or connect more APIs without changing the core logic

## Quick Start

### 1. Install dependencies
```bash
pip install -r requirements.txt
```

### 2. Set up environment variables
Create a `.env` file:
```
GEMINI_API_KEYS=your_gemini_api_key
HUGGINGFACE_API_KEYS=your_hf_key
SPOTIPY_CLIENT_ID=your_spotify_id
SPOTIPY_CLIENT_SECRET=your_spotify_secret
SPOTIPY_REDIRECT_URI=http://localhost:8888/callback
```

### 3. Run the Streamlit UI
```bash
streamlit run streamlit_app.py
```

### 4. Or run the terminal mode
```bash
python main.py
```

## Project Structure

```
Friday_AI_Assistant/
├── streamlit_app.py          # Streamlit frontend entry point
├── main.py                   # Terminal/voice mode entry point
├── config.py                 # Environment config loader
├── requirements.txt
├── .streamlit/
│   └── config.toml           # Streamlit dark theme config
│
├── ui/                       # Streamlit frontend package
│   ├── __init__.py
│   ├── state.py              # Session state init, chat history helpers
│   ├── styles.py             # Custom CSS / dark theme injection
│   ├── loader.py             # Cached LLM, agent, memory loading
│   ├── router.py             # Smart model routing (flash vs pro)
│   ├── context.py            # Memory retrieval + agent input builder
│   └── chat.py               # Message rendering + streaming
│
├── agents/
│   └── friday_agent.py       # LangChain agent with tool-calling
│
├── core/
│   └── llm_engine.py         # Gemini Flash/Pro LLM initialization
│
├── memory/
│   └── memory_manager.py     # FAISS vector store + conversational memory
│
├── tools/
│   └── custom_tools.py       # Weather, Spotify, App/Website openers
│
└── faiss_db/                 # Persistent vector store data
```
