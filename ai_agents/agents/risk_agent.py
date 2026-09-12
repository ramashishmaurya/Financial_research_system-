from ai_agents.state import AgentState
from ai_agents.agents.search_agent import get_llm

def risk_agent_node(state: AgentState):
    """
    Risk Agent: Identifies potential investment risks.
    """
    company_name = state["company_name"]
    raw_data = state["raw_data"]
    
    print(f"[Risk Agent] Identifying risks for {company_name}...")
    
    llm = get_llm(max_tokens=150)
    prompt = f"Based on this data: '{raw_data}', identify exactly 2 critical investment risks for {company_name}. Output them as two short bullet points."
    
    try:
        response = llm.invoke(prompt)
        risk_factors = response.content
    except Exception as e:
        risk_factors = f"Mocked Risks (Error: {str(e)})"
        
    return {"risk_factors": risk_factors}
