# Sentry Trade — Implementation Tracker

## Phase 1: Project Foundation
- [x] Initialise environment with `uv pip`
- [x] Create `requirements.txt`: LangGraph, CrewAI, yfinance, duckduckgo-search, streamlit, pandas, fastapi
- [x] Configure `.env` with `OLLAMA_API_KEY`
- [x] Define `TradingState` TypedDict

## Phase 2: Tooling
- [x] `tools/market_data.py` — stock history and financial metrics via yfinance
- [x] `tools/technical_ind.py` — SMA, EMA, RSI, MACD via pandas
- [x] `tools/search.py` — DuckDuckGo news wrapper
- [x] `tools/correlation.py` — correlation matrix and portfolio metrics
- [x] Tests for all tools in `tests/test_tools.py`

## Phase 3: Agents (Ollama Cloud-powered)
- [x] **Technical Analyst** — system prompt + technical tool set
- [x] **Fundamental Analyst** — system prompt + financial metrics
- [x] **Sentiment Analyst** — system prompt + DuckDuckGo news tool
- [x] **Risk Analyst** — system prompt + volatility tools
- [x] **Judge** — synthesis prompt designed to resolve analyst conflicts
- [x] Unit tests for agents in `tests/test_agents.py`

## Phase 4: LangGraph Orchestration
- [x] Build `StateGraph` with all nodes wired
- [x] Supervisor → parallel analysts → judge execution path
- [x] `test_graph.py` CLI script for tracing execution with Indian tickers
- [x] Compile and test graph invocation

## Phase 5: Multi-Stock (CrewAI)
- [x] Intent classifier and ticker extractor
- [x] Stock Scorer, Correlation Analyst, Portfolio Strategist agents
- [x] Crew runners for compare and portfolio flows
- [x] Router that routes queries to LangGraph or CrewAI based on intent

## Phase 6: Interface
- [x] FastAPI `api.py` with `/health`, `/analyze`, `/smart-analyze`, `/watchlist-scan`
- [x] Streamlit `app.py` with chat I/O and expandable analyst reports
- [x] Sidebar settings (API override, debug toggles)
- [x] Docker Compose for API, Streamlit, and n8n

## Phase 7: Automation & Polish
- [ ] Test pipeline across diverse Indian stocks and sectors
- [ ] Refine agent prompts to reduce hallucinations and improve verdict quality
- [ ] Add error handling for invalid tickers and API timeouts
- [ ] Wire n8n daily scan workflow to Gmail for alert notifications