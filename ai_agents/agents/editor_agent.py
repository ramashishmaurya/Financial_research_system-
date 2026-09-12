from ai_agents.state import AgentState
from ai_agents.agents.search_agent import get_llm

def editor_agent_node(state: AgentState):
    """
    Editor Agent: Compiles all information into a final Markdown report.
    """
    company_name = state["company_name"]
    raw_data = state.get("raw_data", "")
    market_sentiment = state.get("market_sentiment", "")
    risk_factors = state.get("risk_factors", "")
    sentiment = market_sentiment
    risks = risk_factors
    
    print(f"[Editor Agent] Formatting final report for {company_name}...")
    
    llm = get_llm(max_tokens=400)
    prompt = f"""
    You are an elite Financial Editor. Compile the following into a highly professional, beautifully formatted Markdown report for {company_name}.
    Use headings (##), bold text, and bullet points. Keep it under 250 words total to ensure it fits in a 1-page PDF.
    
    Raw Data: {raw_data}
    Sentiment: {sentiment}
    Risks: {risks}
    
    Structure:
    # 🏢 Financial Research Report: {company_name}
    ## 📊 Executive Summary
    ## 📈 Market Sentiment
    ## ⚠️ Investment Risks
    """
    
    try:
        response = llm.invoke(prompt)
        final_report = response.content
    except Exception as e:
        final_report = f"# Error generating report\n\n{str(e)}"
        
    return {"final_report": final_report}
