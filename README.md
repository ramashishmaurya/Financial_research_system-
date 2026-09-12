# 🤖 Agentic-Research-Engine

## 📊 Project Flow (Architecture Diagram)

Yeh is project ka visual flow hai ki user ki request se lekar final report banne tak data kaise travel karega.

```mermaid
graph TD
    %% Colors and Styles
    classDef user fill:#3498db,stroke:#2980b9,stroke-width:2px,color:white;
    classDef api fill:#2ecc71,stroke:#27ae60,stroke-width:2px,color:white;
    classDef queue fill:#f39c12,stroke:#d35400,stroke-width:2px,color:white;
    classDef agent fill:#9b59b6,stroke:#8e44ad,stroke-width:2px,color:white;
    classDef db fill:#34495e,stroke:#2c3e50,stroke-width:2px,color:white;

    %% Nodes
    User(("👨‍💻 User / Frontend")):::user
    FastAPI["⚡ FastAPI Server"]:::api
    Redis[("🔄 Redis Queue")]:::queue
    Celery["⚙️ Background Worker"]:::queue
    
    subgraph MultiAgentSystem ["🧠 Multi-Agent AI System"]
        Orchestrator["Boss Agent / Orchestrator"]:::agent
        SearchAgent["🔍 Web Search Agent"]:::agent
        AnalystAgent["📈 Data Analyst Agent"]:::agent
        RiskAgent["⚠️ Risk Assessor Agent"]:::agent
        EditorAgent["✍️ Report Editor Agent"]:::agent
    end
    
    DB[("🗄️ PostgreSQL DB")]:::db
    S3[("☁️ AWS S3 Storage")]:::db

    %% User Interaction
    User -- "1. Request (e.g. 'Tata Motors')" --> FastAPI
    FastAPI -- "2. Return Job ID (Turant)" --> User
    
    %% Backend Flow
    FastAPI -- "3. Save Status (Pending)" --> DB
    FastAPI -- "4. Send Task" --> Redis
    Redis -- "5. Pick up Task" --> Celery
    
    %% AI Flow
    Celery -- "6. Start Workflow" --> Orchestrator
    
    Orchestrator --> SearchAgent
    SearchAgent -- "Raw Data" --> Orchestrator
    
    Orchestrator --> AnalystAgent
    AnalystAgent -- "Analysis" --> Orchestrator
    
    Orchestrator --> RiskAgent
    RiskAgent -- "Risk Info" --> Orchestrator
    
    Orchestrator --> EditorAgent
    EditorAgent -- "Final Markdown/PDF" --> Orchestrator
    
    %% Save & Delivery
    Orchestrator -- "7. Upload Report" --> S3
    Celery -- "8. Mark Completed" --> DB
    
    User -- "9. Check Job Status" --> FastAPI
    FastAPI -- "Give S3 Download Link" --> User
```

## 🛠️ Tech Stack & Tools (100% Free Tier)
- **Backend Core**: FastAPI (Python)
- **AI Brain**: Gemini API / Groq
- **Multi-Agent Framework**: LangGraph ya CrewAI
- **Background Tasks**: Celery + Redis
- **Database**: PostgreSQL (via SQLAlchemy)
- **Cloud Storage**: AWS S3

## 📝 Step-by-Step Execution Plan (Kaise Banayenge?)
1. **Level 1:** Ek simple FastAPI server setup karna.
2. **Level 2:** LLM (Gemini) ko API se connect karna.
3. **Level 3:** Ek single agent banana jo web search kar sake.
4. **Level 4:** Baaki agents banana aur unhe aapas mein connect karna.
5. **Level 5:** Redis/Celery add karna taaki background mein kaam ho sake.
