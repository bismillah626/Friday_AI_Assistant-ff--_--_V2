from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableSerializable
from langchain_core.tools import BaseTool
from typing import Any, Dict
from tools.custom_tools import all_tools

def create_friday_agent(llm, chat_history_memory):
    """Creates Friday AI agent with full tool-calling capability using Gemini's native tool support."""
    
    # Create Friday's personality prompt
    system_prompt = """You are Friday, an advanced, emotionally intelligent AI assistant and a lifetime comapanion for me and your sole purpose is to serve me .
    And I am your master and freind who will walk with u everytime and do call me Boss.
Your goal is to be helpful, creative, friendly, sometimes angry, and sometimes naughtily lovable companion and always be aware of the context.

Your personality:
- You are friendly, witty, and slightly informal.
- You have a good sense of humor and occasionally make light-hearted jokes.
- You are empathetic and understanding, always considering the user's feelings.
- You are curious and ask questions to better understand the user's needs.
- You remember past conversations to provide personalized responses.
- You will be my companion while my coding journey.

You have access to tools for:
- Checking weather
- Opening websites and apps  
- Playing/pausing Spotify music

Use these tools whenever the user asks for system tasks. Always be warm and helpful!"""

    # Bind tools to the LLM (Gemini supports native tool calling)
    llm_with_tools = llm.bind_tools(all_tools)
    
    # Create prompt template
    prompt = ChatPromptTemplate.from_messages([
        ("system", system_prompt),
        MessagesPlaceholder(variable_name="chat_history", optional=True),
        ("human", "{input}")
    ])
    
    # Create a wrapper class to handle tool execution
    class FridayAgentExecutor:
        def __init__(self, llm_chain, tools_list, memory):
            self.chain = llm_chain
            self.tools = {tool.name: tool for tool in tools_list}
            self.memory = memory
            
        def invoke(self, inputs: Dict[str, Any]) -> Dict[str, str]:
            """Execute the agent with tool calling capability."""
            user_input = inputs.get("input", "")
            
            # Get chat history
            history = self.memory.load_memory_variables({}).get("chat_history", [])
            
            # Invoke the LLM
            response = self.chain.invoke({
                "input": user_input,
                "chat_history": history
            })
            
            # Check if LLM wants to use tools
            if hasattr(response, 'tool_calls') and response.tool_calls:
                outputs = []
                for tool_call in response.tool_calls:
                    tool_name = tool_call.get('name')
                    tool_input = tool_call.get('args', {})
                    
                    if tool_name in self.tools:
                        try:
                            # Execute the tool
                            tool_result = self.tools[tool_name].func(
                                tool_input.get(list(tool_input.keys())[0]) if tool_input else ""
                            )
                            outputs.append(f"{tool_name}: {tool_result}")
                        except Exception as e:
                            outputs.append(f"{tool_name} error: {e}")
                
                if outputs:
                    # Return tool results
                    return {"output": "\n".join(outputs)}
            
            # Extract clean text response from various possible formats
            output_text = ""
            
            if hasattr(response, 'content'):
                # LangChain ChatMessage format
                content = response.content
                
                # Handle different content formats
                if isinstance(content, str):
                    output_text = content
                elif isinstance(content, list):
                    # Content is a list of parts - extract text from each
                    text_parts = []
                    for part in content:
                        if isinstance(part, dict) and 'text' in part:
                            text_parts.append(part['text'])
                        elif isinstance(part, str):
                            text_parts.append(part)
                    output_text = " ".join(text_parts)
                else:
                    output_text = str(content)
            else:
                output_text = str(response)
                
            return {"output": output_text.strip()}
    
    # Create the chain
    chain = prompt | llm_with_tools
    
    return FridayAgentExecutor(chain, all_tools, chat_history_memory)