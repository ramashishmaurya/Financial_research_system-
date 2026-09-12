import os
# pyrefly: ignore [missing-import]
from langchain_groq import ChatGroq
from ai_agents.state import AgentState
# pyrefly: ignore [missing-import]
from tavily import TavilyClient

# Setup the Groq LLM (Ensure GROQ_API_KEY is in .env)
def get_llm(max_tokens=250):
    return ChatGroq(temperature=0.2, model_name="qwen/qwen3.8-27b", max_tokens=max_tokens)

def search_agent_node(state: AgentState):
    """
    Search Agent: Scrapes web for latest financial news and data using Tavily.
    """
    company_name = state["company_name"]
    print(f"[Search Agent] Searching web for data on {company_name} via Tavily...")
    
    # Check if Tavily API Key exists
    tavily_key = os.getenv("TAVILY_API_KEY")
    if not tavily_key or tavily_key == "your_tavily_key_here":
        print("[Search Agent] No Tavily Key found, falling back to LLM knowledge.")
        llm = get_llm()
        response = llm.invoke(f"Give me a 3 sentence summary of {company_name}.")
        return {"raw_data": response.content}
    
    try:
        tavily = TavilyClient(api_key=tavily_key)
        # Search the web for latest news about the company
        search_result = tavily.search(query=f"latest financial news and updates {company_name}", search_depth="basic", max_results=3)
        
        # Compile the search context
        context = ""
        for idx, result in enumerate(search_result.get("results", [])):
            context += f"Source {idx+1} ({result['url']}): {result['content']}\n"
        
        # Use LLM to summarize the search results cleanly
        llm = get_llm(max_tokens=200)
        prompt = f"Extract the most crucial real-time financial facts about {company_name} from the following data. Keep it highly concise (under 100 words):\n\n{context}"
        response = llm.invoke(prompt)
        
        raw_data = response.content
    except Exception as e:
        raw_data = f"Error during Tavily search for {company_name}: {str(e)}"
        
    return {"raw_data": raw_data}
