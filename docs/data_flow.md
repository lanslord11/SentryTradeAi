# Sentry Trade — Data Flow

This document traces how a query moves through the system from input to final recommendation.

## 1. Input Layer

**Streamlit (`app.py`) → `TradingState`**

1. User submits a query like *"Analyze RELIANCE.NS for a swing trade"*
2. `app.py` creates a `TradingState` dict, populating only `user_query`; all analysis fields start empty
3. The state is passed to the compiled LangGraph in `graph/workflow.py`

## 2. Intent Routing

**FastAPI (`core/classifier.py`) or Streamlit**

1. `classify_intent()` calls Ollama to determine the query type:
   - `single_stock_analysis` → LangGraph path
   - `compare_stocks` / `portfolio_allocation` / `portfolio_analysis` → CrewAI path
2. For CrewAI routes, `extract_tickers()` parses the query and normalises tickers with `.NS`/`.BO` suffixes

## 3. Single-Stock Pipeline (LangGraph)

### Supervisor Node
- Reads `user_query`, extracts the ticker symbol
- Writes `ticker` to state and routes to the four analyst nodes

### Technical Analyst
1. Calls `get_stock_history(ticker, period="3mo")` via yfinance
2. Feeds OHLCV DataFrame into `add_all_indicators()` → SMA, EMA, RSI, MACD appended
3. Ollama reads the raw indicators and drafts a technical summary
4. Writes to `technical_analysis` in state

### Fundamental Analyst
1. Calls `get_financial_metrics(ticker)` via yfinance → P/E, EPS, margins, debt/equity, ROE
2. Ollama evaluates valuation and writes a health summary
3. Writes to `fundamental_analysis` in state

### Sentiment Analyst
1. Calls `search_financial_news(query)` via DuckDuckGo → top headlines + snippets
2. Ollama gauges bullish/bearish sentiment
3. Writes to `sentiment_analysis` in state

### Risk Analyst
1. Calls `get_financial_metrics(ticker)` → beta, 52-week range, debt/equity
2. Ollama evaluates risk profile relative to NIFTY50
3. Writes to `risk_analysis` in state

All four run in parallel. LangGraph waits for all to complete before advancing.

### Judge Node
1. Reads all four `*_analysis` fields from state
2. Ollama synthesises, resolves any conflicts (e.g., Technical says BUY, Fundamental says SELL)
3. Writes `final_recommendation` as BUY / HOLD / SELL

## 4. Multi-Stock Pipeline (CrewAI)

1. `extract_tickers()` normalises the stock list
2. **Stock Scorer** agent loops over each ticker and invokes the full LangGraph pipeline
3. **Correlation Analyst** builds a 6-month price correlation matrix and checks sector diversity
4. **Portfolio Strategist** synthesises scores, correlations, and diversification into a ranked allocation
5. CrewAI runner returns the final portfolio recommendation

## 5. Output

**LangGraph / CrewAI → `app.py` → Streamlit UI**

1. The full state (or CrewAI result) is returned to `app.py`
2. Each analyst's report is rendered in expandable sections
3. The final verdict is displayed prominently in the chat window