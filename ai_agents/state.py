from typing import TypedDict, Annotated, Sequence
import operator

# The State represents the data that gets passed between all agents
class AgentState(TypedDict):
    company_name: str
    raw_data: str                # Populated by Search Agent
    market_sentiment: str        # Populated by Analyst Agent
    risk_factors: str            # Populated by Risk Agent
    final_report: str            # Populated by Editor Agent
