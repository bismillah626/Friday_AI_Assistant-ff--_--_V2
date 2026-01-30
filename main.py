import speech_recognition as sr
import os
import tempfile
import time
from gtts import gTTS

# --- Wake Word and Other Constants ---
WAKE_WORD = "friday"
TIMEOUT_SECONDS = 60  # Wake word not required if active within last 60 seconds

# --- Initialize Speech Engine ---
from agents.friday_agent import create_friday_agent
from memory.memory_manager import MemoryManager
from core.llm_engine import get_flash_llm, get_pro_llm 
from langchain_core.prompts import PromptTemplate

# --- Wake Word and Other Constants ---
WAKE_WORD = "friday"

# Global mode tracker
voice_mode = False

def speak(text: str):
    """Converts text to speech using Google TTS with natural female voice."""
    # Always print the full text with emojis and formatting
    print(f"Friday: {text}")
    
    # Only play audio in voice mode
    if not voice_mode:
        return
    
    try:
        # Clean text for TTS - remove emojis and markdown formatting
        import re
        
        # Remove emojis (unicode emoji ranges)
        emoji_pattern = re.compile("["
            u"\U0001F600-\U0001F64F"  # emoticons
            u"\U0001F300-\U0001F5FF"  # symbols & pictographs
            u"\U0001F680-\U0001F6FF"  # transport & map symbols
            u"\U0001F1E0-\U0001F1FF"  # flags (iOS)
            u"\U00002702-\U000027B0"
            u"\U000024C2-\U0001F251"
            "]+", flags=re.UNICODE)
        clean_text = emoji_pattern.sub('', text)
        
        # Remove markdown formatting (asterisks, underscores)
        clean_text = re.sub(r'\*+', '', clean_text)  # Remove asterisks
        clean_text = re.sub(r'_+', '', clean_text)   # Remove underscores
        clean_text = re.sub(r'`+', '', clean_text)   # Remove backticks
        
        # Remove extra whitespace
        clean_text = re.sub(r'\s+', ' ', clean_text).strip()
        
        # Only speak if there's actual text left
        if clean_text:
            # Create Google TTS with British English accent (sounds more natural and feminine)
            tts = gTTS(text=clean_text, lang='en', tld='co.uk', slow=False)
            
            # Save to temporary file
            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp3') as fp:
                temp_file = fp.name
                tts.save(temp_file)
            
            # Play using mpg123 (already installed on your system)
            os.system(f"mpg123 -q '{temp_file}' 2>/dev/null")
            
            # Clean up
            os.remove(temp_file)
    except Exception as e:
        print(f"[TTS Error] {e}")

def listen() -> str:
    """Listens for a user's command *after* the wake word is detected."""
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("\nListening for your command...")
        r.pause_threshold = 1
        r.adjust_for_ambient_noise(source)
        audio = r.listen(source)

    try:
        print("Recognizing command...")
        query = r.recognize_google(audio, language='en-in')
        print(f"You: {query}")
        return query.lower()
    except Exception:
        return ""

def select_model(user_input: str, llm) -> str:
    """Uses a fast LLM to decide if a query requires a powerful model."""
    prompt_template = """
    You are a decision-making AI that routes user queries to the correct model.
    Based on the user's query, decide if a standard, fast model is sufficient or if a more powerful, in-depth model is required.

    - Queries asking for simple facts, jokes, opening websites, playing music, or weather should use the 'standard' model.
    - Queries that use phrases like 'explain in detail', 'comprehensive analysis', 'break it down for me', 'in depth', or ask complex, multi-step reasoning questions should use the 'powerful' model.

    User Query: "{query}"

    Respond with only the single word: 'standard' or 'powerful'.
    """
    
    prompt = PromptTemplate(template=prompt_template, input_variables=["query"])
    # Use LCEL (LangChain Expression Language) instead of deprecated LLMChain
    router_chain = prompt | llm
    
    response = router_chain.invoke({"query": user_input})
    
    # Extract text from response
    if hasattr(response, 'content'):
        decision_text = response.content
    else:
        decision_text = str(response)
        
    decision = decision_text.strip().lower()
    
    if "powerful" in decision:
        return "powerful"
    return "standard"

# --- Main Interaction Loop ---
if __name__ == "__main__":
    memory_manager = MemoryManager()
    
    print("Initializing LLM models...")
    flash_llm = get_flash_llm()
    pro_llm = get_pro_llm()

    print("Creating agent instances...")
    flash_agent = create_friday_agent(flash_llm, memory_manager.conversational_memory)
    pro_agent = create_friday_agent(pro_llm, memory_manager.conversational_memory)

    speak("Initializing Friday AI. Say my name to activate.")
    
    mode = input("Choose mode: 'v' for voice or 't' for text: ").strip().lower()
    
    # Set voice_mode variable (already global at module level)
    voice_mode = (mode == 'v')
    
    # Track last interaction time for timeout-based wake word
    last_interaction_time = 0  # Start with 0 to require initial wake word

    while True:
        user_input = ""
        
        if mode == 'v':
            current_time = time.time()
            time_since_last_interaction = current_time - last_interaction_time
            
            # Check if wake word is needed (first time or after timeout)
            if time_since_last_interaction > TIMEOUT_SECONDS:
                # Need wake word
                r = sr.Recognizer()
                with sr.Microphone() as source:
                    print(f"\n🔴 Listening for wake word '{WAKE_WORD}'...")
                    r.pause_threshold = 1
                    r.adjust_for_ambient_noise(source)
                    try:
                        audio = r.listen(source, phrase_time_limit=2)
                        heard_phrase = r.recognize_google(audio).lower()

                        if WAKE_WORD in heard_phrase:
                            speak("I'm here. I'll stay active for the next minute.")
                            last_interaction_time = time.time()
                            user_input = listen()
                        else:
                            continue
                    except sr.UnknownValueError:
                        continue
                    except Exception as e:
                        print(f"Error during wake word detection: {e}")
                        continue
            else:
                # Within timeout window - skip wake word
                remaining_time = int(TIMEOUT_SECONDS - time_since_last_interaction)
                print(f"\n🟢 Friday is active (timeout in {remaining_time}s). Speak your command:")
                user_input = listen()
        else:
            user_input = input("You: ").strip().lower()

        if "exit" in user_input or "quit" in user_input:
            speak("Goodbye! Shutting down.")
            break
            
        if user_input:
            chosen_model = select_model(user_input, flash_llm)

            if chosen_model == "powerful":
                print("[System] 🧠 Using gemini-2.5-pro (Powerful model)")
                speak("Okay, this requires a more detailed answer.")
                active_agent = pro_agent
            else:
                #print("[System] ⚡ Using gemini-2.5-flash (Fast model)")
                active_agent = flash_agent

            retriever = memory_manager.get_vector_retriever()
            retrieved_docs = retriever.invoke(user_input)
            retrieved_context = "\n".join([doc.page_content for doc in retrieved_docs])
            
            agent_input = (
                f"Relevant context from past conversations:\n"
                f"{retrieved_context}\n\n"
                f"User's current query: {user_input}"
            )
            
            response = active_agent.invoke({"input": agent_input})
            speak(response['output'])
            memory_manager.save_interaction(user_input, response['output'])
            
            # Update last interaction time to reset timeout window
            last_interaction_time = time.time()