import os
from langchain_community.vectorstores import FAISS
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_core.messages import HumanMessage, AIMessage

# Simple custom memory class since ConversationBufferMemory isn't available
class SimpleConversationalMemory:
    """Simple chat history manager."""
    def __init__(self):
        self.messages = []
    
    def load_memory_variables(self, inputs):
        """Return chat history."""
        return {"chat_history": self.messages}
    
    def save_context(self, inputs, outputs):
        """Save a conversation turn."""
        if "input" in inputs:
            self.messages.append(HumanMessage(content=inputs["input"]))
        if "output" in outputs:
            self.messages.append(AIMessage(content=outputs["output"]))

class MemoryManager:
    """Manages conversational memory and long term vector memory."""
    def __init__(self):
        #initializing the embedding model
        self.embedding_function = HuggingFaceEmbeddings(
            model_name="all-MiniLM-L6-v2")
        
        #initializing FAISS for persistent long term memory
        self.faiss_index_path = "./faiss_db"
        
        # Load existing FAISS index if it exists, otherwise create a new one
        if os.path.exists(os.path.join(self.faiss_index_path, "index.faiss")):
            self.vector_store = FAISS.load_local(
                self.faiss_index_path,
                self.embedding_function,
                allow_dangerous_deserialization=True
            )
        else:
            # Create a new FAISS index with a dummy document
            self.vector_store = FAISS.from_texts(
                ["Friday AI Assistant initialized"],
                self.embedding_function
            )
            
        #initializing short term conversational memory (custom implementation)
        self.conversational_memory = SimpleConversationalMemory()

    def get_vector_retriever(self):
        """Returns the vector store as a retriever for similarity searches."""
        return self.vector_store.as_retriever(search_kwargs={"k": 3})

    def save_interaction(self, user_input: str, ai_response: str):
        """Saves a user-AI interaction to the vector store."""
        interaction_text = f"User asked: {user_input}\nFriday responded: {ai_response}"
        self.vector_store.add_texts([interaction_text])
        
        # Save the updated FAISS index to disk
        os.makedirs(self.faiss_index_path, exist_ok=True)
        self.vector_store.save_local(self.faiss_index_path)
        
        print(f"[Memory] Saved interaction to Vector DB.")

   