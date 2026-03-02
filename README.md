# Financial Datasets MCP Server

## Introduction

This is a Model Context Protocol (MCP) server that provides access to stock market data from [Financial Datasets](https://www.financialdatasets.ai/), [Alpha Vantage](https://www.alphavantage.co/), and [Zerodha Kite](https://kite.trade/). 

It allows Claude and other AI assistants to retrieve global technicals, historical data, and act as a fully-featured trading assistant for the Indian Stock Market (NSE/BSE).

## Available Tools

This MCP server provides the following tools:
- **get_income_statements**: Get income statements for a company.
- **get_balance_sheets**: Get balance sheets for a company.
- **get_cash_flow_statements**: Get cash flow statements for a company.
- **get_current_stock_price**: Get the current / latest price of a company.
- **get_historical_stock_prices**: Gets historical stock prices for a company.
- **get_company_news**: Get news for a company.
- **get_available_crypto_tickers**: Gets all available crypto tickers.
- **get_crypto_prices**: Gets historical prices for a crypto currency.
- **get_historical_crypto_prices**: Gets historical prices for a crypto currency.
- **get_current_crypto_price**: Get the current / latest price of a crypto currency.

### Alpha Vantage Tools
- **search_symbols**: Search for stock symbols and companies matching keywords.
- **get_alpha_vantage_quote**: Get real-time price and volume for a ticker.
- **get_alpha_vantage_intraday**: Get intraday time series (1min, 5min, etc.).
- **get_alpha_vantage_daily**: Get daily historical prices.
- **get_company_overview**: Get company info, ratios, and description.
- **get_alpha_vantage_fundamentals**: Get fundamental data (Income Statement, Balance Sheet, etc.).
- **get_alpha_vantage_news**: Get market news and sentiment analysis.
- **get_currency_exchange_rate**: Get real-time FX or Crypto exchange rates.
- **get_technical_indicator**: Get technical indicators (SMA, RSI, EMA, etc.).

### Zerodha Kite Tools (Indian Market)
*Note: Requires active Kite Connect subscription.*
- **kite_login**: Get the Zerodha login URL for authentication.
- **kite_generate_session**: Exchange the request token for a session proxy.
- **kite_get_profile**: Get user account profile.
- **kite_get_margins**: Check available funds for trading (Equity/Commodity).
- **kite_get_holdings**: Get long-term portfolio stock holdings.
- **kite_get_positions**: Get current day/overnight trading positions.
- **kite_get_orders**: Get the list of all orders.
- **kite_get_quote**: Get real-time quotes for NSE/BSE instruments.
- **kite_get_historical_data**: Get historical OHLC data.
- **kite_place_order**: Place a new market/limit order.

## Setup

### Prerequisites

- Python 3.10 or higher
- [uv](https://github.com/astral-sh/uv) package manager

### Installation

1. Clone this repository:
   ```bash
   git clone https://github.com/financial-datasets/mcp-server
   cd mcp-server
   ```

2. If you don't have uv installed, install it:
   ```bash
   # macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   curl -LsSf https://astral.sh/uv/install.ps1 | powershell
   ```

3. Install dependencies:
   ```bash
   # Create virtual env and activate it
   uv venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Install dependencies
   uv add "mcp[cli]" httpx  # On Windows: uv add mcp[cli] httpx

   ```

4. Set up environment variables:
   ```bash
   # Create .env file for your API keys
   cp .env.example .env

    # Set API keys in .env
    FINANCIAL_DATASETS_API_KEY=your-financial-datasets-api-key
    ALPHA_VANTAGE_API_KEY=your-alpha-vantage-api-key
    KITE_API_KEY=your-kite-api-key
    KITE_API_SECRET=your-kite-api-secret
   ```

5. Run the server:
   ```bash
   uv run server.py
   ```

## Connecting to Claude Desktop

1. Install [Claude Desktop](https://claude.ai/desktop) if you haven't already

2. Create or edit the Claude Desktop configuration file:
   ```bash
   # macOS
   mkdir -p ~/Library/Application\ Support/Claude/
   nano ~/Library/Application\ Support/Claude/claude_desktop_config.json
   ```

3. Add the following configuration:
   ```json
   {
     "mcpServers": {
       "financial-datasets": {
         "command": "/path/to/uv",
         "args": [
           "--directory",
           "/absolute/path/to/financial-datasets-mcp",
           "run",
           "server.py"
         ]
       }
     }
   }
   ```
   
   Replace `/path/to/uv` with the result of `which uv` and `/absolute/path/to/financial-datasets-mcp` with the absolute path to this project.

4. Restart Claude Desktop

5. You should now see the financial tools available in Claude Desktop's tools menu (hammer icon)

6. Try asking Claude questions like:
   - "What are Apple's recent income statements?"
   - "Show me the current price of Tesla stock"
   ---

## Roadmap & Contributions

Interested in contributing? We have an ambitious roadmap focusing on:
1. 🇮🇳 **Indian Market Integration** (NSE/BSE support)
2. 🧠 **Intelligent Data Pre-processing** (pandas-ta indicators)
3. ⚡ **Performance & Caching Layer**
4. 🗞️ **Sentiment & Macro Signals**

Check out the [ROADMAP.md](ROADMAP.md) for a full breakdown of planned features and how you can help!

