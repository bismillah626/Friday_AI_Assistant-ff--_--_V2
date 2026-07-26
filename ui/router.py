"""Wraps the existing select_model routing logic from main.py."""

from langchain_core.prompts import PromptTemplate


ROUTER_TEMPLATE = """
You are a decision-making AI that routes user queries to the correct model.
Based on the user's query, decide if a standard, fast model is sufficient or if a more powerful, in-depth model is required.

- Queries asking for simple facts, jokes, opening websites, playing music, or weather should use the 'standard' model.
- Queries that use phrases like 'explain in detail', 'comprehensive analysis', 'break it down for me', 'in depth', or ask complex, multi-step reasoning questions should use the 'powerful' model.

User Query: "{query}"

Respond with only the single word: 'standard' or 'powerful'.
"""


def route_query(user_input: str, flash_llm):
    """Decide whether to use flash or pro model. Returns 'standard' or 'powerful'."""
    prompt = PromptTemplate(template=ROUTER_TEMPLATE, input_variables=["query"])
    chain = prompt | flash_llm
    response = chain.invoke({"query": user_input})

    text = response.content if hasattr(response, "content") else str(response)
    decision = text.strip().lower()

    if "powerful" in decision:
        return "powerful"
    return "standard"
