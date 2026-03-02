# 🚀 Roadmap: Scaling Findata-MCP for the Indian Market & Beyond

First off, thank you for checking out this project! The goal of `findata-mcp-server` is to provide a standardized Model Context Protocol interface for professional financial data. To take this from a hobbyist tool to a robust analyst assistant, we are planning the following upgrades.

We’ve identified four key "pillars" for improvement and are looking for contributors to help lead these modules.

## 1. 🇮🇳 Indian Market Integration (High Priority)
While the current core supports global/US data, we want to make this the go-to MCP server for the Indian Stock Market (NSE/BSE).

*   ✅ **Completed:** Integrated [Zerodha Kite Connect API](./README.md#zerodha-kite-tools-indian-market) for live portfolio and market data streaming.
*   **Task:** Add a `BreezeProvider` or `UpstoxProvider` for users who do not use Zerodha.
*   **Task:** Implement a fallback mechanism using `yfinance` for users without any API keys.
*   **Contribution Level:** Intermediate (Python, API Integration)

## 2. 🧠 Intelligent Data Pre-processing
LLMs are great at reasoning but mediocre at math. We want the server to do the heavy lifting before passing data to the model.

*   **Task:** Integrate `pandas-ta` to provide pre-computed technical indicators (RSI, MACD, Bollinger Bands) as tool outputs.
*   **Task:** Add a "Support & Resistance" tool that identifies key price levels using historical pivots.
*   **Contribution Level:** Intermediate (Data Science, Pandas)

## 3. ⚡ Performance & Caching Layer
To respect API rate limits (especially for free tiers like Alpha Vantage) and improve LLM response speed.

*   **Task:** Implement a local caching layer (SQLite or Redis) with configurable TTL (Time-to-Live).
*   **Task:** Add "Batch Tools" to fetch data for multiple tickers in a single LLM tool call.
*   **Contribution Level:** Advanced (System Design, Backend)

## 4. 🗞️ Sentiment & Macro Signals
Quant data only tells half the story. We need qualitative "vibe" checks.

*   **Task:** Add a `SentimentTool` that fetches and summarizes recent news headlines for a specific ticker.
*   **Task:** Integrate Indian macro indicators (RBI Repo Rates, Inflation data) via official sources.
*   **Contribution Level:** Beginner/Intermediate (NLP, Web Scraping)

## How to Contribute
1. Comment on the relevant issue/discussion about which feature you’d like to work on so we can avoid overlapping work.
2. Draft a PR (even if it's a Work-In-Progress) so we can provide feedback early.
3. Check out `CONTRIBUTING.md` (coming soon) for coding standards.

What features are we missing? Let us know in the issues! 👇
