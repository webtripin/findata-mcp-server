import json
import os
import httpx
import logging
import sys
from mcp.server.fastmcp import FastMCP
from dotenv import load_dotenv

# Configure logging to write to stderr
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    stream=sys.stderr,
)
logger = logging.getLogger("financial-datasets-mcp")

# Initialize FastMCP server
mcp = FastMCP("financial-datasets")

FINANCIAL_DATASETS_API_BASE = "https://api.financialdatasets.ai"
ALPHA_VANTAGE_API_BASE = "https://www.alphavantage.co/query"


async def make_request(url: str) -> dict[str, any] | None:
    """Make a request to the Financial Datasets API with proper error handling."""
    # Load environment variables from .env file
    load_dotenv()
    
    headers = {}
    if api_key := os.environ.get("FINANCIAL_DATASETS_API_KEY"):
        headers["X-API-KEY"] = api_key

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url, headers=headers, timeout=30.0)
            response.raise_for_status()
            return response.json()
        except Exception as e:
            return {"Error": str(e)}


async def make_alpha_vantage_request(params: dict[str, str]) -> dict[str, any] | None:
    """Make a request to the Alpha Vantage API with proper error handling."""
    # Load environment variables from .env file
    load_dotenv()
    
    api_key = os.environ.get("ALPHA_VANTAGE_API_KEY")
    if not api_key:
        return {"Error": "Alpha Vantage API key not found in environment variables."}

    # Add apikey to parameters
    params["apikey"] = api_key

    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(ALPHA_VANTAGE_API_BASE, params=params, timeout=30.0)
            response.raise_for_status()
            data = response.json()
            
            # Alpha Vantage returns errors in a "Note" or "Error Message" key
            if "Note" in data:
                return {"Error": f"API Limit Reached or Note: {data['Note']}"}
            if "Error Message" in data:
                return {"Error": data["Error Message"]}
            if "Information" in data:
                 return {"Error": data["Information"]}
                
            return data
        except Exception as e:
            return {"Error": str(e)}


@mcp.tool()
async def get_income_statements(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
) -> str:
    """Get income statements for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        period: Period of the income statement (e.g. annual, quarterly, ttm)
        limit: Number of income statements to return (default: 4)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/income-statements/?ticker={ticker}&period={period}&limit={limit}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch income statements or no income statements found."

    # Extract the income statements
    income_statements = data.get("income_statements", [])

    # Check if income statements are found
    if not income_statements:
        return "Unable to fetch income statements or no income statements found."

    # Stringify the income statements
    return json.dumps(income_statements, indent=2)


@mcp.tool()
async def get_balance_sheets(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
) -> str:
    """Get balance sheets for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        period: Period of the balance sheet (e.g. annual, quarterly, ttm)
        limit: Number of balance sheets to return (default: 4)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/balance-sheets/?ticker={ticker}&period={period}&limit={limit}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch balance sheets or no balance sheets found."

    # Extract the balance sheets
    balance_sheets = data.get("balance_sheets", [])

    # Check if balance sheets are found
    if not balance_sheets:
        return "Unable to fetch balance sheets or no balance sheets found."

    # Stringify the balance sheets
    return json.dumps(balance_sheets, indent=2)


@mcp.tool()
async def get_cash_flow_statements(
    ticker: str,
    period: str = "annual",
    limit: int = 4,
) -> str:
    """Get cash flow statements for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        period: Period of the cash flow statement (e.g. annual, quarterly, ttm)
        limit: Number of cash flow statements to return (default: 4)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/financials/cash-flow-statements/?ticker={ticker}&period={period}&limit={limit}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch cash flow statements or no cash flow statements found."

    # Extract the cash flow statements
    cash_flow_statements = data.get("cash_flow_statements", [])

    # Check if cash flow statements are found
    if not cash_flow_statements:
        return "Unable to fetch cash flow statements or no cash flow statements found."

    # Stringify the cash flow statements
    return json.dumps(cash_flow_statements, indent=2)


@mcp.tool()
async def get_current_stock_price(ticker: str) -> str:
    """Get the current / latest price of a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/prices/snapshot/?ticker={ticker}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch current price or no current price found."

    # Extract the current price
    snapshot = data.get("snapshot", {})

    # Check if current price is found
    if not snapshot:
        return "Unable to fetch current price or no current price found."

    # Stringify the current price
    return json.dumps(snapshot, indent=2)


@mcp.tool()
async def get_historical_stock_prices(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "day",
    interval_multiplier: int = 1,
) -> str:
    """Gets historical stock prices for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        start_date: Start date of the price data (e.g. 2020-01-01)
        end_date: End date of the price data (e.g. 2020-12-31)
        interval: Interval of the price data (e.g. minute, hour, day, week, month)
        interval_multiplier: Multiplier of the interval (e.g. 1, 2, 3)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/prices/?ticker={ticker}&interval={interval}&interval_multiplier={interval_multiplier}&start_date={start_date}&end_date={end_date}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch prices or no prices found."

    # Extract the prices
    prices = data.get("prices", [])

    # Check if prices are found
    if not prices:
        return "Unable to fetch prices or no prices found."

    # Stringify the prices
    return json.dumps(prices, indent=2)


@mcp.tool()
async def get_company_news(ticker: str) -> str:
    """Get news for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/news/?ticker={ticker}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch news or no news found."

    # Extract the news
    news = data.get("news", [])

    # Check if news are found
    if not news:
        return "Unable to fetch news or no news found."
    return json.dumps(news, indent=2)


@mcp.tool()
async def get_available_crypto_tickers() -> str:
    """
    Gets all available crypto tickers.
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/tickers"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch available crypto tickers or no available crypto tickers found."

    # Extract the available crypto tickers
    tickers = data.get("tickers", [])

    # Stringify the available crypto tickers
    return json.dumps(tickers, indent=2)


@mcp.tool()
async def get_crypto_prices(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "day",
    interval_multiplier: int = 1,
) -> str:
    """
    Gets historical prices for a crypto currency.
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/?ticker={ticker}&interval={interval}&interval_multiplier={interval_multiplier}&start_date={start_date}&end_date={end_date}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch prices or no prices found."

    # Extract the prices
    prices = data.get("prices", [])

    # Check if prices are found
    if not prices:
        return "Unable to fetch prices or no prices found."

    # Stringify the prices
    return json.dumps(prices, indent=2)


@mcp.tool()
async def get_historical_crypto_prices(
    ticker: str,
    start_date: str,
    end_date: str,
    interval: str = "day",
    interval_multiplier: int = 1,
) -> str:
    """Gets historical prices for a crypto currency.

    Args:
        ticker: Ticker symbol of the crypto currency (e.g. BTC-USD). The list of available crypto tickers can be retrieved via the get_available_crypto_tickers tool.
        start_date: Start date of the price data (e.g. 2020-01-01)
        end_date: End date of the price data (e.g. 2020-12-31)
        interval: Interval of the price data (e.g. minute, hour, day, week, month)
        interval_multiplier: Multiplier of the interval (e.g. 1, 2, 3)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/?ticker={ticker}&interval={interval}&interval_multiplier={interval_multiplier}&start_date={start_date}&end_date={end_date}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch prices or no prices found."

    # Extract the prices
    prices = data.get("prices", [])

    # Check if prices are found
    if not prices:
        return "Unable to fetch prices or no prices found."

    # Stringify the prices
    return json.dumps(prices, indent=2)


@mcp.tool()
async def get_current_crypto_price(ticker: str) -> str:
    """Get the current / latest price of a crypto currency.

    Args:
        ticker: Ticker symbol of the crypto currency (e.g. BTC-USD). The list of available crypto tickers can be retrieved via the get_available_crypto_tickers tool.
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/crypto/prices/snapshot/?ticker={ticker}"
    data = await make_request(url)

    # Check if data is found
    if not data:
        return "Unable to fetch current price or no current price found."

    # Extract the current price
    snapshot = data.get("snapshot", {})

    # Check if current price is found
    if not snapshot:
        return "Unable to fetch current price or no current price found."

    # Stringify the current price
    return json.dumps(snapshot, indent=2)


@mcp.tool()
async def get_sec_filings(
    ticker: str,
    limit: int = 10,
    filing_type: str | None = None,
) -> str:
    """Get all SEC filings for a company.

    Args:
        ticker: Ticker symbol of the company (e.g. AAPL, GOOGL)
        limit: Number of SEC filings to return (default: 10)
        filing_type: Type of SEC filing (e.g. 10-K, 10-Q, 8-K)
    """
    # Fetch data from the API
    url = f"{FINANCIAL_DATASETS_API_BASE}/filings/?ticker={ticker}&limit={limit}"
    if filing_type:
        url += f"&filing_type={filing_type}"
 
    # Call the API
    data = await make_request(url)

    # Extract the SEC filings
    filings = data.get("filings", [])

    # Check if SEC filings are found
    if not filings:
        return f"Unable to fetch SEC filings or no SEC filings found."

    # Stringify the SEC filings
    return json.dumps(filings, indent=2)


# --- Alpha Vantage Tools ---

@mcp.tool()
async def search_symbols(keywords: str) -> str:
    """Search for stock symbols and companies matching the keywords.
    
    Args:
        keywords: The keywords to search for (e.g., 'microsoft', 'BA').
    """
    params = {
        "function": "SYMBOL_SEARCH",
        "keywords": keywords
    }
    data = await make_alpha_vantage_request(params)
    if "Error" in data:
        return f"Error: {data['Error']}"
    
    matches = data.get("bestMatches", [])
    if not matches:
        return f"No symbols found matching '{keywords}'."
    
    return json.dumps(matches, indent=2)


@mcp.tool()
async def get_alpha_vantage_quote(symbol: str) -> str:
    """Get the latest price and volume information for a specific stock ticker.
    
    Args:
        symbol: The ticker symbol (e.g., AAPL).
    """
    params = {
        "function": "GLOBAL_QUOTE",
        "symbol": symbol
    }
    data = await make_alpha_vantage_request(params)
    if "Error" in data:
        return f"Error: {data['Error']}"
    
    quote = data.get("Global Quote", {})
    if not quote:
        return f"No quote found for symbol '{symbol}'."
    
    return json.dumps(quote, indent=2)


@mcp.tool()
async def get_alpha_vantage_intraday(symbol: str, interval: str = "5min") -> str:
    """Get intraday time series (price and volume) for a stock.
    
    Args:
        symbol: The ticker symbol (e.g., TSLA).
        interval: Time interval between data points (1min, 5min, 15min, 30min, 60min).
    """
    params = {
        "function": "TIME_SERIES_INTRADAY",
        "symbol": symbol,
        "interval": interval
    }
    data = await make_alpha_vantage_request(params)
    if "Error" in data:
        return f"Error: {data['Error']}"
    
    time_series_key = f"Time Series ({interval})"
    time_series = data.get(time_series_key, {})
    
    if not time_series:
        return f"No intraday data found for symbol '{symbol}' at interval '{interval}'."
    
    # Return first 100 entries to avoid overwhelming output
    limited_series = dict(list(time_series.items())[:100])
    return json.dumps({
        "metadata": data.get("Meta Data", {}),
        "time_series": limited_series
    }, indent=2)


@mcp.tool()
async def get_alpha_vantage_daily(symbol: str, outputsize: str = "compact") -> str:
    """Get daily time series (price and volume) for a stock.
    
    Args:
        symbol: The ticker symbol (e.g., MSFT).
        outputsize: 'compact' (last 100 points) or 'full' (up to 20 years).
    """
    params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": symbol,
        "outputsize": outputsize
    }
    data = await make_alpha_vantage_request(params)
    if "Error" in data:
        return f"Error: {data['Error']}"
    
    time_series = data.get("Time Series (Daily)", {})
    if not time_series:
         return f"No daily data found for symbol '{symbol}'."
         
    return json.dumps({
        "metadata": data.get("Meta Data", {}),
        "time_series": time_series
    }, indent=2)


@mcp.tool()
async def get_company_overview(symbol: str) -> str:
    """Get company information, financial ratios, and business description.
    
    Args:
        symbol: The ticker symbol (e.g., AAPL).
    """
    params = {
        "function": "OVERVIEW",
        "symbol": symbol
    }
    data = await make_alpha_vantage_request(params)
    if "Error" in data:
        return f"Error: {data['Error']}"
    
    if not data:
        return f"No overview data found for symbol '{symbol}'."
    
    return json.dumps(data, indent=2)


@mcp.tool()
async def get_alpha_vantage_fundamentals(symbol: str, report_type: str = "INCOME_STATEMENT") -> str:
    """Get fundamental data for a company (Income Statement, Balance Sheet, Cash Flow, Earnings).
    
    Args:
        symbol: The ticker symbol (e.g., IBM).
        report_type: One of 'INCOME_STATEMENT', 'BALANCE_SHEET', 'CASH_FLOW', 'EARNINGS'.
    """
    if report_type not in ["INCOME_STATEMENT", "BALANCE_SHEET", "CASH_FLOW", "EARNINGS"]:
         return "Error: report_type must be one of 'INCOME_STATEMENT', 'BALANCE_SHEET', 'CASH_FLOW', 'EARNINGS'."
         
    params = {
        "function": report_type,
        "symbol": symbol
    }
    data = await make_alpha_vantage_request(params)
    if "Error" in data:
        return f"Error: {data['Error']}"
    
    if not data:
        return f"No fundamental data ({report_type}) found for symbol '{symbol}'."
    
    return json.dumps(data, indent=2)


@mcp.tool()
async def get_alpha_vantage_news(tickers: str | None = None, topics: str | None = None, limit: int = 10) -> str:
    """Get market news and sentiment analysis.
    
    Args:
        tickers: Ticker symbols to filter by (e.g., 'AAPL,TSLA').
        topics: News topics to filter by (e.g., 'technology', 'ipo', 'earnings').
        limit: Number of news results (default 10, max 1000).
    """
    params = {
        "function": "NEWS_SENTIMENT",
        "limit": str(limit)
    }
    if tickers:
        params["tickers"] = tickers
    if topics:
        params["topics"] = topics
        
    data = await make_alpha_vantage_request(params)
    if "Error" in data:
        return f"Error: {data['Error']}"
    
    feed = data.get("feed", [])
    if not feed:
        return "No news found with the specified filters."
        
    return json.dumps(feed, indent=2)


@mcp.tool()
async def get_currency_exchange_rate(from_currency: str, to_currency: str) -> str:
    """Get the real-time exchange rate for a pair of currencies (physical or digital).
    
    Args:
        from_currency: The currency you are converting from (e.g., 'USD', 'BTC').
        to_currency: The currency you are converting to (e.g., 'EUR', 'CNY').
    """
    params = {
        "function": "CURRENCY_EXCHANGE_RATE",
        "from_currency": from_currency,
        "to_currency": to_currency
    }
    data = await make_alpha_vantage_request(params)
    if "Error" in data:
        return f"Error: {data['Error']}"
    
    rate = data.get("Realtime Currency Exchange Rate", {})
    if not rate:
        return f"No exchange rate found for {from_currency} to {to_currency}."
        
    return json.dumps(rate, indent=2)


@mcp.tool()
async def get_technical_indicator(symbol: str, indicator: str, interval: str = "daily", time_period: int = 60, series_type: str = "close") -> str:
    """Get technical indicators for a stock (e.g., SMA, RSI, EMA).
    
    Args:
        symbol: The ticker symbol (e.g., AAPL).
        indicator: The indicator name (e.g., 'SMA', 'EMA', 'RSI', 'ADX').
        interval: Time interval (1min, 5min, 15min, 30min, 60min, daily, weekly, monthly).
        time_period: Number of data points used to calculate the indicator.
        series_type: The price type in the time series (close, open, high, low).
    """
    params = {
        "function": indicator.upper(),
        "symbol": symbol,
        "interval": interval,
        "time_period": str(time_period),
        "series_type": series_type
    }
    data = await make_alpha_vantage_request(params)
    if "Error" in data:
        return f"Error: {data['Error']}"
    
    indicator_data = data.get(f"Technical Analysis: {indicator.upper()}", {})
    if not indicator_data:
        return f"No data found for indicator {indicator} on {symbol}."
        
    # Return last 100 entries
    limited_data = dict(list(indicator_data.items())[:100])
    return json.dumps({
        "metadata": data.get("Meta Data", {}),
        "indicator_data": limited_data
    }, indent=2)


if __name__ == "__main__":
    # Log server startup
    logger.info("Starting Financial Datasets MCP Server...")

    # Initialize and run the server
    mcp.run(transport="stdio")

    # This line won't be reached during normal operation
    logger.info("Server stopped")
