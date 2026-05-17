# Sentry Trade — Architecture Blueprint

## Overview

Sentry Trade is a multi-agent equity analysis platform for Indian markets. It uses local LLM inference via Ollama Cloud to power two parallel execution paths: LangGraph for single-stock deep analysis, and CrewAI for multi-stock portfolio work.

The architecture prioritises keeping inference local and cost-free, relying on free data sources (yfinance, DuckDuckGo) rather than paid APIs.

## Core Components

### 1. Language Model
- **Provider:** Ollama Cloud
- **Role:** All reasoning, synthesis, classification, and judgment runs through Ollama—no external LLM APIs required

### 2. User Interface
- **Streamlit** — lightweight Python-native chat interface
- **FastAPI** — REST endpoints for automation and external integrations

### 3. Orchestration Layer
- **LangGraph** — manages the single-stock pipeline with typed state, parallel node execution, and a supervisor-based router
- **CrewAI** — handles multi-stock workflows (compare, rank, allocate) via a sequential agent process

### 4. Agent Layer
Four specialist agents run in parallel under LangGraph:

- **Technical Analyst** — price action, moving averages, RSI, MACD, volume
- **Fundamental Analyst** — P/E, EPS, debt/equity, revenue, margins
- **Sentiment Analyst** — live news via DuckDuckGo, analyst commentary
- **Risk Analyst** — beta, volatility, sector exposure, macro signals

A **Judge** node synthesises the four reports into a final BUY / HOLD / SELL verdict.

### 5. Data Sources (free)

| Source | Library | Used for |
|--------|---------|----------|
| Market data | yfinance | OHLCV, financials, ratios |
| News & sentiment | DuckDuckGo Search | Headlines, earnings news |
| LLM inference | Ollama Cloud | All reasoning tasks |

## Execution Flow

1. **Query received** via Streamlit or FastAPI
2. **Intent router** (`classify_intent`) classifies as single-stock, compare, or portfolio
3. **Single-stock path** (LangGraph):
   - Supervisor extracts ticker
   - Four analysts run in parallel
   - Judge synthesises verdict
4. **Multi-stock path** (CrewAI):
   - Ticker extraction
   - Stock Scorer runs LangGraph per ticker
   - Correlation & diversification analysis
   - Portfolio strategist produces ranked allocation
5. **Response** returned to UI with individual analyst reports and final verdict