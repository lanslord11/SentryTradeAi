# Sentry Trade — Agent & Tool Reference

Each agent's inputs, outputs, and the tools they invoke.

## Agent Summary

| Agent | Focus | State Output |
|-------|-------|-------------|
| Technical Analyst | Price action & indicators | `technical_analysis` |
| Fundamental Analyst | Company health & valuation | `fundamental_analysis` |
| Sentiment Analyst | News & market mood | `sentiment_analysis` |
| Risk Analyst | Volatility & risk profile | `risk_analysis` |
| Judge | Synthesis & final verdict | `final_recommendation` |

---

## Technical Analyst
**Input:** `{"ticker": str}`
**Output:** `{"technical_analysis": str}`

**Tools:**
1. `get_stock_history(ticker, period)` → OHLCV DataFrame (Date, Open, High, Low, Close, Volume)
2. `add_all_indicators(df)` → DataFrame with SMA_20, SMA_50, EMA_20, RSI_14, MACD columns appended

---

## Fundamental Analyst
**Input:** `{"ticker": str}`
**Output:** `{"fundamental_analysis": str}`

**Tools:**
1. `get_financial_metrics(ticker)` → Dict with `marketCap`, `peRatio`, `eps`, `dividendYield`, `profitMargins`, `debtToEquity`, `roe`, `revenueGrowth`

---

## Sentiment Analyst
**Input:** `{"ticker": str, "user_query": str}`
**Output:** `{"sentiment_analysis": str}`

**Tools:**
1. `search_financial_news(query, max_results)` → List of Dict objects each containing `title`, `snippet`, `date`, `source`, `url`

---

## Risk Analyst
**Input:** `{"ticker": str}`
**Output:** `{"risk_analysis": str}`

**Tools:**
1. `get_financial_metrics(ticker)` → Reads `beta`, `fiftyTwoWeekHigh`, `fiftyTwoWeekLow`, `debtToEquity` from the returned dict

---

## Judge
**Input:** Full `TradingState` with all four `*_analysis` fields populated
**Output:** `{"final_recommendation": str}` — must end with BUY, HOLD, or SELL

**Tools:** None. Pure LLM synthesis node.