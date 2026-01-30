from langchain_google_genai import ChatGoogleGenerativeAI
from config import GOOGLE_API_KEY, HUGGINGFACE_API_KEYS
from langchain_huggingface import HuggingFaceEndpoint

def get_pro_llm():
    """Initialize and return the Gemini-2.5-pro LLM (most powerful)."""
    return ChatGoogleGenerativeAI(
        model = "gemini-2.5-pro",
        google_api_key = GOOGLE_API_KEY,
        temperature = 0.75,
        convert_system_message_to_human=True 
        )
def get_flash_llm():
    """Initialize and return the Gemini-2.5-flash LLM (fast)."""
    return ChatGoogleGenerativeAI(
        model = "gemini-2.5-flash",
        google_api_key = GOOGLE_API_KEY,
        temperature = 0.75,
        convert_system_message_to_human=True     
    )

def get_huggingface_llm(repo_id="mistralai/Mixtral-8x7B-Instruct-v0.1", temp=0.7):
    """Initialize and return a HuggingFace Hub LLM."""
    
    return HuggingFaceEndpoint(
        repo_id=repo_id,
        huggingfacehub_api_token=HUGGINGFACE_API_KEYS,
        model_kwargs={"temperature": temp},
        task="text-generation" 
    )
