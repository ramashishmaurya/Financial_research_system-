from langgraph.graph import StateGraph, END
from ai_agents.state import AgentState
from ai_agents.agents.search_agent import search_agent_node
from ai_agents.agents.analyst_agent import analyst_agent_node
from ai_agents.agents.risk_agent import risk_agent_node
from ai_agents.agents.editor_agent import editor_agent_node

def build_research_graph():
    # 1. Initialize Graph
    graph = StateGraph(AgentState)
    
    # 2. Add Nodes (Agents)
    graph.add_node("SearchAgent", search_agent_node)
    graph.add_node("AnalystAgent", analyst_agent_node)
    graph.add_node("RiskAgent", risk_agent_node)
    graph.add_node("EditorAgent", editor_agent_node)
    
    # 3. Define Flow (Edges)
    # The flow is: Start -> Search -> (Analyst & Risk in parallel technically, but we'll do sequential for simplicity) -> Editor -> End
    graph.set_entry_point("SearchAgent")
    graph.add_edge("SearchAgent", "AnalystAgent")
    graph.add_edge("SearchAgent", "RiskAgent")
    
    # Since we can't easily merge paths in basic langgraph without conditional edges, 
    # Let's make it sequential to keep it simple for now:
    # Search -> Analyst -> Risk -> Editor
    # Let's override the above edges:
    
    # Resetting the graph for a sequential flow
    graph = StateGraph(AgentState)
    graph.add_node("Search", search_agent_node)
    graph.add_node("Analyst", analyst_agent_node)
    graph.add_node("Risk", risk_agent_node)
    graph.add_node("Editor", editor_agent_node)
    
    graph.set_entry_point("Search")
    graph.add_edge("Search", "Analyst")
    graph.add_edge("Analyst", "Risk")
    graph.add_edge("Risk", "Editor")
    graph.add_edge("Editor", END)
    
    # 4. Compile Graph
    return graph.compile()

def run_research_pipeline(company_name: str) -> str:
    """
    Kicks off the Multi-Agent LangGraph workflow.
    Returns the final Markdown report.
    """
    app = build_research_graph()
    
    initial_state = {"company_name": company_name}
    
    print(f"[Orchestrator] Starting Multi-Agent workflow for: {company_name}")
    final_state = app.invoke(initial_state)
    
    return final_state["final_report"]
