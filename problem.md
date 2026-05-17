# Sentry Trade — Design Overview

Sentry Trade is an Indian equity analysis agent that combines multi-agent orchestration with local LLM inference. The system accepts natural-language stock queries, routes them to the appropriate agent pipeline, and returns structured Buy/Hold/Sell verdicts.

This document covers the high-level architecture, state design, execution flow, and the reasoning behind the technology choices.

---

## Architecture Layers

### Layer 1 — Gateway

A FastAPI layer (or Streamlit chat UI) accepts the user's query. It initializes the runtime state and dispatches to the orchestration layer. This is intentionally thin—it holds no business logic.

### Layer 2 — Orchestration (LangGraph)

LangGraph's `StateGraph` manages execution flow. It holds the shared state object across all agents, handles branching (parallel analyst runs), and manages joins before synthesis.

A lightweight **Supervisor** node runs first. It extracts the ticker symbol from the raw query and seeds the state. This decouples ticker extraction from the analyst agents themselves, making it easy to swap or improve routing logic without touching agents.

### Layer 3 — Multi-Agent Analysts (LangChain + LangGraph Nodes)

Each analyst is a LangGraph node backed by a LangChain `AgentExecutor`. They share the same state object but run independently.

- **Technical Analyst** — pulls OHLCV data via yfinance, computes RSI, MACD, moving averages, and volume profiles
- **Fundamental Analyst** — fetches P/E ratios, EPS, revenue growth, debt metrics, and sector benchmarks from yfinance
- **Sentiment Analyst** — runs live DuckDuckGo searches for recent headlines, earnings calls, and analyst commentary
- **Risk Analyst** — evaluates beta, volatility (ATR/ATR%), sector exposure, and macro signals (interest rates, FII flows)

Each analyst writes its findings directly into the shared state. No inter-agent communication is needed—the graph handles coordination.

### Layer 4 — Data Layer

- **yfinance** — the primary data source for OHLCV, financials, and market metrics
- **DuckDuckGo Search** — powers real-time news and sentiment lookups without API keys
- **Ollama Cloud** — runs all LLM inference (prompting, synthesis, classification)

---

## State Design

All data flows through a single typed state object:

```python
from typing import TypedDict, Annotated
from operator import add

class TradingState(TypedDict):
    user_query: str
    ticker: str
    fundamental_analysis: str
    technical_analysis: str
    sentiment_analysis: str
    risk_analysis: str
    final_recommendation: str
    messages: Annotated[list, add]
```

`messages` uses the `add` reducer so each agent's thought process accumulates rather than overwrites—useful for debugging and audit trails.

---

## Execution Flow

```
START → Supervisor
         ↓
   [Tickers extracted, state seeded]
         ↓
    ═════ PARALLEL BRANCH ═════
    ↓         ↓         ↓         ↓
Tech    Fundamental  Sentiment   Risk
    ↓         ↓         ↓         ↓
    ═══════════ JOIN ════════════
              ↓
         Judge Node
    (synthesizes all reports)
              ↓
           END
```

1. **Supervisor** extracts ticker from `user_query`, updates state
2. **Parallel analysts** run simultaneously, each writing to their own field
3. **Join** — LangGraph waits for all four to complete
4. **Judge** reads the four analysis fields, resolves conflicts, outputs `final_recommendation`

---

## Why This Architecture

**Parallel execution via LangGraph** keeps latency low. All four analysts run concurrently rather than sequentially querying tools one by one.

**Shared state design** makes the system auditable. Every agent's output is in the state object. If the final verdict looks wrong, you can trace it back to a specific analyst and understand exactly why.

**Separation of agents** keeps the codebase maintainable. Each analyst has a narrow focus and a single toolset. Swapping out a data provider or updating a system prompt doesn't require touching the graph or other agents.

**Ollama Cloud** keeps inference local and cost-free while still delivering strong reasoning for financial analysis tasks.

**Intent routing** lets the same API surface handle both "Should I buy HDFC?" and "Compare TCS and INFY" without separate endpoints.