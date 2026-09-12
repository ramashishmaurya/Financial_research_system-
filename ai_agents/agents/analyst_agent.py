from ai_agents.state import AgentState
from ai_agents.agents.search_agent import get_llm

def analyst_agent_node(state: AgentState):
    """
    Analyst Agent: Analyzes raw data for market sentiment.
    """
    company_name = state["company_name"]
    raw_data = state["raw_data"]
    
    print(f"[Analyst Agent] Analyzing sentiment for {company_name}...")
    
    llm = get_llm(max_tokens=150)
    prompt = f"Based on this data: '{raw_data}', what is the overall market sentiment (Bullish/Bearish/Neutral) for {company_name}? Give a concise 2-sentence explanation."
    
    try:
        response = llm.invoke(prompt)
        market_sentiment = response.content
    except Exception as e:
        market_sentiment = f"Mocked Sentiment (Error: {str(e)})"
        
    return {"market_sentiment": market_sentiment}
