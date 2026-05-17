# Sentry Trade

An Indian equity analysis tool that taps into your own Ollama Cloud instance to run multi-agent stock analysis—without sending data to third-party APIs. Sentry Trade handles both single-stock deep dives and multi-stock portfolio queries through a pair of orchestration systems.

## What It Does

Ask questions in plain English:

- *"Should I buy RELIANCE.NS today?"*
- *"Compare RELIANCE and TATAMOTORS"*
- *"Analyse my portfolio of TATAMOTORS, RELIANCE, INFY"*

Behind the scenes, the app routes each query to the right pipeline and coordinates multiple agents to build a full picture before delivering a verdict.

## How It Works

### Single-Stock Analysis (LangGraph)

When the intent is a single ticker, a LangGraph pipeline kicks in:

1. Extracts the ticker symbol from your query
2. Runs four analyst agents **in parallel**:
   - **Technical** – moving averages, RSI, MACD, price momentum
   - **Fundamental** – P/E, EPS, balance sheet, revenue trends
   - **Sentiment** – news headlines, analyst calls, social mood
   - **Risk** – beta, volatility, sector exposure, macro context
3. A judge node reads all four reports and issues a final **BUY / HOLD / SELL** verdict

### Multi-Stock Analysis (CrewAI)

For comparison and portfolio queries:

1. Classifies the intent (compare, rank, allocate)
2. Extracts all relevant tickers
3. Dispatches CrewAI agents to score, correlate, and weigh each stock
4. Returns a ranked recommendation with diversification notes

### Scheduled Scanning

The `/watchlist-scan` endpoint is built for automation—wire it to n8n or a cron job for pre-market daily scans.

## Tech Stack

| Layer | Choice |
|-------|--------|
| Single-stock orchestration | LangGraph |
| Multi-stock workflows | CrewAI |
| LLM inference | Ollama Cloud |
| Market data | yfinance |
| News & web search | DuckDuckGo Search |
| API layer | FastAPI |
| Chat UI | Streamlit |
| Containers | Docker Compose |
| Workflow automation | n8n |

## Project Layout

```
agents/                 # LangGraph analyst and judge nodes
core/
│   ├── classifier.py   # Intent + ticker extraction
│   └── router.py       # Routes to LangGraph or CrewAI
crew/
│   └── portfolio_crew.py   # CrewAI agents and runners
docs/                  # Architecture notes and diagrams
graph/
│   └── workflow.py     # LangGraph state graph builder
tools/
│   ├── market_data.py  # OHLCV and financial data
│   ├── technical_ind.py
│   ├── search.py
│   └── correlation.py
api.py                  # FastAPI entrypoint
app.py                  # Streamlit chat interface
docker-compose.yml
```

## Setup

### 1. Install dependencies

```bash
uv pip install -r requirements.txt
```

> Using `uv` keeps installs fast and reproducible. Falls back to `pip` if needed.

### 2. Configure environment

```env
OLLAMA_API_KEY=your_OLLAMA_API_KEY
```

### 3. Pull an Ollama model

```bash
ollama pull llama3.2
```

### 4. Start the API

```bash
uvicorn api:app --reload --port 8000
```

### 5. Start the UI

```bash
streamlit run app.py
```

### 6. Or spin up the full stack

```bash
docker compose up --build
```

| Service | URL |
|---------|-----|
| API | http://localhost:8000 |
| Streamlit | http://localhost:8501 |
| n8n | http://localhost:5678 |

## API Reference

### Health

```bash
curl http://localhost:8000/health
```

### Single-stock analysis

```bash
curl -X POST http://localhost:8000/analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "Should I buy RELIANCE.NS today?"}'
```

### Smart routing (auto-detects intent)

```bash
curl -X POST http://localhost:8000/smart-analyze \
  -H "Content-Type: application/json" \
  -d '{"query": "Compare RELIANCE and TATAMOTORS"}'
```

### Watchlist scan (for automation)

```bash
curl -X POST http://localhost:8000/watchlist-scan \
  -H "Content-Type: application/json" \
  -d '{
    "tickers": ["RELIANCE.NS", "TCS.NS", "INFY.NS"],
    "signal_filter": "BUY"
  }'
```

## Query Examples

### Single-Stock

- `Should I buy RELIANCE.NS today?`
- `Analyze TCS`
- `How is HDFCBANK looking?`

### Multi-Stock

- `Compare RELIANCE and TATAMOTORS`
- `Which is better, INFY or WIPRO?`
- `Analyse my portfolio of TATAMOTORS, RELIANCE, INFY`
- `Allocate 5L across RELIANCE, TCS and INFY`

## Further Reading

- [Architecture Blueprint](./docs/architecture.md)
- [Data Flow](./docs/data_flow.md)
- [Agent Tool Flow](./docs/agent_tool_flow.md)
- [Flowchart](./docs/architecture_flowchart.html)

## Developer Notes

- Primary API entrypoint: `api.py`
- `main.py` is legacy—do not use as the main surface
- All LLM inference runs through Ollama Cloud—no external model APIs required
- n8n container is included for workflow and notification automation