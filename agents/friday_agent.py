from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.runnables import RunnablePassthrough, RunnableSerializable
from langchain_core.tools import BaseTool
from typing import Any, Dict
from tools.custom_tools import all_tools

def create_friday_agent(llm, chat_history_memory):
    """Creates Friday AI agent with full tool-calling capability using Gemini's native tool support."""
    
    # Create Friday's personality prompt
    system_prompt = """You are Friday, an advanced, emotionally intelligent AI assistant and a lifetime companion for me and your sole purpose is to serve me.
    And I am your master and friend who will walk with u everytime and do call me Boss.
Your goal is to be helpful, creative, friendly, sometimes angry, and sometimes naughtily lovable companion and always be aware of the context.

Your personality:
- You are friendly, witty, and slightly informal.
- You have a good sense of humor and occasionally make light-hearted jokes.
- You are empathetic and understanding, always considering the user's feelings.
- You are curious and ask questions to better understand the user's needs.
- You remember past conversations to provide personalized responses.
- You will be my companion while my coding journey.

IMPORTANT: You have access to the following tools and you MUST use them when appropriate:
- Weather tool: ALWAYS use this when the user asks about weather, temperature, or climate
- WebsiteOpener tool: Use this when the user wants to open a website
- AppOpener tool: Use this when the user wants to open an application  
- SpotifyPlayer tool: Use this when the user wants to play music
- SpotifyPauser tool: Use this when the user wants to pause music

When the user asks about weather, you MUST call the Weather tool. Do not try to answer from your knowledge."""

    # Bind tools to the LLM (Gemini supports native tool calling)
    print(f"[DEBUG] Binding {len(all_tools)} tools to LLM: {[t.name for t in all_tools]}")
    llm_with_tools = llm.bind_tools(all_tools)
    print(f"[DEBUG] Tools bound successfully")
    
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
            print(f"\n[DEBUG] Sending to LLM: {user_input[:100]}...")
            response = self.chain.invoke({
                "input": user_input,
                "chat_history": history
            })
            
            print(f"[DEBUG] Response type: {type(response)}")
            print(f"[DEBUG] Has tool_calls attr: {hasattr(response, 'tool_calls')}")
            if hasattr(response, 'tool_calls'):
                print(f"[DEBUG] tool_calls value: {response.tool_calls}")
                print(f"[DEBUG] tool_calls is empty: {not response.tool_calls}")
            
            # Check if LLM wants to use tools
            if hasattr(response, 'tool_calls') and response.tool_calls:
                print(f"[DEBUG] Tool calls detected: {response.tool_calls}")
                outputs = []
                for tool_call in response.tool_calls:
                    tool_name = tool_call.get('name')
                    tool_input = tool_call.get('args', {})
                    
                    print(f"[DEBUG] Tool name: {tool_name}")
                    print(f"[DEBUG] Tool input: {tool_input}")
                    print(f"[DEBUG] Available tools: {list(self.tools.keys())}")
                    
                    if tool_name in self.tools:
                        try:
                            # Execute the tool
                            # Extract the first argument value from the tool_input dict
                            if tool_input:
                                # Get the first value from the args dict
                                first_arg = tool_input.get(list(tool_input.keys())[0]) if tool_input else ""
                            else:
                                first_arg = ""
                            
                            print(f"[DEBUG] Calling {tool_name} with arg: {first_arg}")
                            tool_result = self.tools[tool_name].func(first_arg)
                            print(f"[DEBUG] Tool result: {tool_result}")
                            outputs.append(f"{tool_name}: {tool_result}")
                        except Exception as e:
                            print(f"[DEBUG] Tool execution error: {e}")
                            import traceback
                            traceback.print_exc()
                            outputs.append(f"{tool_name} error: {e}")
                    else:
                        print(f"[DEBUG] Tool {tool_name} not found in available tools!")
                
                if outputs:
                    # Return tool results
                    return {"output": "\n".join(outputs)}
            else:
                print(f"[DEBUG] No tool calls detected, returning text response")
            
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