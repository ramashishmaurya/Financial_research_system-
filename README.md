# Agentic Financial Research Engine

A production-ready, asynchronous multi-agent AI system designed to generate comprehensive financial research reports. It leverages the power of LangGraph for orchestrating specialized AI agents, Celery and Redis for asynchronous background processing, and FastAPI for robust API routing.

## 🚀 Features

- **Multi-Agent Architecture (LangGraph):** Employs a relay-race methodology across four specialized AI agents:
  - `Search Agent`: Fetches real-time market data and news using the Tavily Search API.
  - `Analyst Agent`: Derives market sentiment (Bullish/Bearish) and extracts key insights.
  - `Risk Agent`: Identifies critical investment risks and red flags.
  - `Editor Agent`: Synthesizes data into a professional, cohesive Markdown report.
- **Asynchronous Processing:** Powered by **Celery** and **Redis**. API endpoints return instantly (yielding a `job_id`), preventing browser timeouts while intensive AI tasks run in the background.
- **Web Dashboard View:** Real-time polling updates the UI gracefully, rendering the final Markdown report directly into a beautifully styled HTML dashboard via `marked.js` with zero forced PDF downloads.
- **Persistent Storage:** Uses **SQLite** (via SQLAlchemy) to track job queues, timestamps, and store raw report content. Easily scalable to PostgreSQL.
- **Token Optimized:** Custom agent constraints ensure the system remains well within strict LLM API output token limits (e.g., Groq's Free Tier).

## 🏗️ System Architecture

```mermaid
graph LR
    A[Client UI] -->|POST /research| B(FastAPI Server)
    B -->|Returns job_id| A
    B -->|Enqueues Task| C((Redis Broker))
    D[Celery Worker] -->|Pulls Task| C
    D -->|Executes| E[LangGraph Multi-Agent Pipeline]
    E <--> F[(SQLite Database)]
    A -->|GET /status/{job_id}| B
    B -->|Reads Status/Report| F
```

## 📋 Prerequisites

Before you begin, ensure you have the following installed:
- Python 3.10+
- Redis Server (Must be running locally or via Docker)
- API Keys: [Groq](https://console.groq.com/) (LLM), [Tavily](https://tavily.com/) (Search)

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/yourusername/financial-research-system.git
   cd financial-research-system
   ```

2. **Set up a virtual environment (Optional but recommended):**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure Environment Variables:**
   Create a `.env` file in the root directory and add your credentials:
   ```env
   # API Keys
   GROQ_API_KEY=your_groq_api_key_here
   TAVILY_API_KEY=your_tavily_api_key_here

   # Database (SQLite for local testing)
   DATABASE_URL=sqlite:///./research_engine.db

   # Redis Configuration
   REDIS_URL=redis://localhost:6379/0
   ```

## 🚦 Running the Application

This architecture requires two separate terminals to run the API and the background worker simultaneously.

**Terminal 1: Start the FastAPI Server**
```bash
uvicorn backend.main:app --reload
```
*The API will be available at `http://127.0.0.1:8000`. You can view the Swagger UI at `/docs`.*

**Terminal 2: Start the Celery Worker**
```bash
# On Windows (using solo pool):
celery -A worker.celery_app worker -l info -P solo

# On Linux/Mac:
celery -A worker.celery_app worker -l info
```

**Terminal 3: Launch the Frontend**
You can serve the frontend folder using any simple HTTP server.
```bash
cd frontend
python -m http.server 3000
```
*Open `http://localhost:3000` in your web browser to access the dashboard.*

## 🛣️ Future Scope
- **User Authentication:** Integrate JWT-based login (Schema is already prepared in `auth_table.py`).
- **AWS S3 Integration:** Offload old reports to S3 cold storage for database cost optimization.
- **Chart Generation:** Enable AI to generate matplotlib graphics and embed them via S3 URLs into the dashboard.

## 📄 License
MIT License.
