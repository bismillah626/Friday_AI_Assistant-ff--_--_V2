"""Memory retriever + agent_input builder — mirrors main.py's context injection."""


def build_agent_input(user_input: str, memory_manager):
    """Retrieve relevant past context and format the agent input string."""
    retriever = memory_manager.get_vector_retriever()
    docs = retriever.invoke(user_input)
    context = "\n".join(doc.page_content for doc in docs)

    return (
        f"Relevant context from past conversations:\n"
        f"{context}\n\n"
        f"User's current query: {user_input}"
    )


def save_interaction(user_input: str, response_text: str, memory_manager):
    """Persist the exchange to vector memory — same as main.py does."""
    memory_manager.save_interaction(user_input, response_text)
