"""TinkClaw MCP Server — exposes TinkClaw financial API as MCP tools."""

import json
import os
from typing import Any

import requests
from mcp.server.fastmcp import FastMCP

BASE_URL = "https://api.tinkclaw.com/v1"

mcp = FastMCP(
    "TinkClaw",
    description="Financial signals, market regime, risk metrics, and more from TinkClaw API",
)


def _api_key() -> str:
    key = os.environ.get("TINKCLAW_API_KEY", "")
    if not key:
        raise ValueError("TINKCLAW_API_KEY environment variable is not set")
    return key


def _get(path: str, params: dict[str, Any] | None = None) -> dict:
    """Make an authenticated GET request to the TinkClaw API."""
    try:
        resp = requests.get(
            f"{BASE_URL}{path}",
            params=params,
            headers={"X-API-Key": _api_key()},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.HTTPError as e:
        code = e.response.status_code if e.response is not None else "unknown"
        body = ""
        if e.response is not None:
            try:
                body = e.response.json().get("error", e.response.text[:200])
            except Exception:
                body = e.response.text[:200]
        return {"error": f"HTTP {code}: {body}"}
    except requests.ConnectionError:
        return {"error": "Connection failed — is the API reachable?"}
    except requests.Timeout:
        return {"error": "Request timed out after 30s"}
    except ValueError as e:
        return {"error": str(e)}
    except Exception as e:
        return {"error": f"Unexpected error: {type(e).__name__}: {e}"}


def _post(path: str, body: dict[str, Any] | None = None) -> dict:
    """Make an authenticated POST request to the TinkClaw API."""
    try:
        resp = requests.post(
            f"{BASE_URL}{path}",
            json=body,
            headers={"X-API-Key": _api_key()},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.HTTPError as e:
        code = e.response.status_code if e.response is not None else "unknown"
        body_text = ""
        if e.response is not None:
            try:
                body_text = e.response.json().get("error", e.response.text[:200])
            except Exception:
                body_text = e.response.text[:200]
        return {"error": f"HTTP {code}: {body_text}"}
    except Exception as e:
        return {"error": f"Unexpected error: {type(e).__name__}: {e}"}


def _delete(path: str) -> dict:
    """Make an authenticated DELETE request to the TinkClaw API."""
    try:
        resp = requests.delete(
            f"{BASE_URL}{path}",
            headers={"X-API-Key": _api_key()},
            timeout=30,
        )
        resp.raise_for_status()
        return resp.json()
    except requests.HTTPError as e:
        code = e.response.status_code if e.response is not None else "unknown"
        body_text = ""
        if e.response is not None:
            try:
                body_text = e.response.json().get("error", e.response.text[:200])
            except Exception:
                body_text = e.response.text[:200]
        return {"error": f"HTTP {code}: {body_text}"}
    except Exception as e:
        return {"error": f"Unexpected error: {type(e).__name__}: {e}"}


def _fmt(data: dict) -> str:
    """Format API response as readable JSON."""
    return json.dumps(data, indent=2, default=str)


# ---------------------------------------------------------------------------
# Core tools — one per API endpoint
# ---------------------------------------------------------------------------


@mcp.tool()
def get_signals(symbol: str) -> str:
    """Get trading signals (BUY/SELL/HOLD with confidence) for a symbol.

    Args:
        symbol: Ticker symbol, e.g. BTCUSD, AAPL, EURUSD
    """
    return _fmt(_get("/signals", {"symbol": symbol}))


@mcp.tool()
def get_signals_ml(symbols: str) -> str:
    """Get ML-enhanced trading signals for one or more symbols.

    Args:
        symbols: Comma-separated ticker symbols, e.g. BTCUSD,ETHUSD,AAPL
    """
    return _fmt(_get("/signals-ml", {"symbols": symbols}))


@mcp.tool()
def get_regime(symbol: str) -> str:
    """Get market regime classification (trending/calm/volatile/crisis) for a symbol.

    Args:
        symbol: Ticker symbol, e.g. BTCUSD, AAPL
    """
    return _fmt(_get("/regime", {"symbol": symbol}))


@mcp.tool()
def get_confluence(symbol: str) -> str:
    """Get 6-layer confluence score for a symbol. Higher = stronger signal agreement.

    Args:
        symbol: Ticker symbol, e.g. BTCUSD, AAPL
    """
    return _fmt(_get("/confluence", {"symbol": symbol}))


@mcp.tool()
def get_indicators(symbols: str, range_days: int = 30) -> str:
    """Get technical indicators (RSI, MACD, Bollinger Bands) for symbols.

    Args:
        symbols: Comma-separated ticker symbols, e.g. BTCUSD,AAPL
        range_days: Number of days of historical data (default: 30)
    """
    return _fmt(_get("/indicators", {"symbols": symbols, "range": range_days}))


@mcp.tool()
def get_risk_metrics(symbols: str) -> str:
    """Get risk metrics (Sharpe ratio, VaR, Sortino ratio, max drawdown) for symbols.

    Args:
        symbols: Comma-separated ticker symbols, e.g. BTCUSD,ETHUSD
    """
    return _fmt(_get("/risk-metrics", {"symbols": symbols}))


@mcp.tool()
def get_correlation(symbols: str) -> str:
    """Get correlation matrix between symbols.

    Args:
        symbols: Comma-separated ticker symbols (at least 2), e.g. BTCUSD,ETHUSD,AAPL
    """
    return _fmt(_get("/correlation", {"symbols": symbols}))


@mcp.tool()
def get_screener() -> str:
    """Get all 62 supported symbols ranked by signal strength. No arguments needed."""
    return _fmt(_get("/screener"))


@mcp.tool()
def get_ecosystem() -> str:
    """Get cross-asset correlations and systemic risk overview. No arguments needed."""
    return _fmt(_get("/ecosystem"))


@mcp.tool()
def get_order_flow(symbol: str) -> str:
    """Get order flow data for a symbol (Pro plan required).

    Args:
        symbol: Ticker symbol, e.g. BTCUSD, AAPL
    """
    return _fmt(_get(f"/flow/{symbol}"))


@mcp.tool()
def get_news(symbol: str) -> str:
    """Get financial news related to a symbol.

    Args:
        symbol: Ticker symbol, e.g. BTCUSD, AAPL
    """
    return _fmt(_get("/news", {"symbol": symbol}))


@mcp.tool()
def get_market_summary() -> str:
    """Get a broad market overview across all asset classes. No arguments needed."""
    return _fmt(_get("/market-summary"))


@mcp.tool()
def get_backtest(symbol: str, strategy: str = "hurst_momentum", days: int = 365) -> str:
    """Run a backtest on a symbol with a given strategy.

    Args:
        symbol: Ticker symbol, e.g. BTCUSD
        strategy: Strategy name (default: hurst_momentum)
        days: Lookback period in days (default: 365)
    """
    return _fmt(_get("/backtest", {"symbol": symbol, "strategy": strategy, "days": days}))


@mcp.tool()
def get_hurst_history(symbol: str, days: int = 365, window: int = 60) -> str:
    """Get Hurst exponent time series for a symbol. Values > 0.5 indicate trending behavior.

    Args:
        symbol: Ticker symbol, e.g. BTCUSD
        days: Lookback period in days (default: 365)
        window: Rolling window size in days (default: 60)
    """
    return _fmt(_get("/hurst-history", {"symbol": symbol, "days": days, "window": window}))


@mcp.tool()
def get_symbols() -> str:
    """List all supported symbols (stocks, crypto, forex, commodities, indices)."""
    return _fmt(_get("/symbols"))


@mcp.tool()
def get_health() -> str:
    """Check TinkClaw API health status."""
    return _fmt(_get("/health"))


# ---------------------------------------------------------------------------
# Composite tools — chain multiple endpoints
# ---------------------------------------------------------------------------


@mcp.tool()
def get_morning_brief() -> str:
    """Get a morning market brief: market summary, ecosystem risk, and top screener picks.

    Chains market-summary + ecosystem + screener into one call. No arguments needed.
    """
    summary = _get("/market-summary")
    ecosystem = _get("/ecosystem")
    screener = _get("/screener")

    return _fmt({
        "market_summary": summary,
        "ecosystem": ecosystem,
        "screener_top_10": screener.get("data", screener)[:10] if isinstance(screener.get("data", screener), list) else screener,
    })


@mcp.tool()
def deep_dive(symbol: str) -> str:
    """Deep dive into a single symbol: signals, regime, technical indicators, and risk metrics.

    Args:
        symbol: Ticker symbol, e.g. BTCUSD, AAPL
    """
    signals = _get("/signals", {"symbol": symbol})
    regime = _get("/regime", {"symbol": symbol})
    indicators = _get("/indicators", {"symbols": symbol, "range": 30})
    risk = _get("/risk-metrics", {"symbols": symbol})

    return _fmt({
        "symbol": symbol,
        "signals": signals,
        "regime": regime,
        "indicators": indicators,
        "risk_metrics": risk,
    })


@mcp.tool()
def alpha_scan() -> str:
    """Scan for high-conviction opportunities: screener results filtered to confidence > 70%.

    Returns only symbols where signal confidence exceeds 70%. No arguments needed.
    """
    screener = _get("/screener")

    items = screener.get("data", screener)
    if not isinstance(items, list):
        return _fmt(screener)

    high_conf = []
    for item in items:
        conf = item.get("confidence", 0)
        if isinstance(conf, (int, float)) and conf > 70:
            high_conf.append(item)

    return _fmt({
        "total_scanned": len(items),
        "high_conviction_count": len(high_conf),
        "threshold": "70%",
        "results": high_conf,
    })


# ---------------------------------------------------------------------------
# Bot Training / Feedback Loop tools
# ---------------------------------------------------------------------------


@mcp.tool()
def get_my_predictions(status: str = "all", symbol: str = "", limit: int = 50) -> str:
    """Get your prediction history with outcomes — the core feedback loop for learning.

    Shows resolved predictions with hit/miss status, P&L, and regime at prediction time.
    Use this to analyze which conditions lead to wins vs losses.

    Args:
        status: Filter by "all", "active", "hit", or "missed"
        symbol: Filter to a specific symbol (e.g., "BTC"), empty for all
        limit: Max results 1-100 (default 50)
    """
    params = {"status": status, "limit": limit}
    if symbol:
        params["symbol"] = symbol.upper()
    return _fmt(_get("/agent/me/predictions", params))


@mcp.tool()
def get_my_stats(group_by: str = "symbol") -> str:
    """Get your aggregated performance stats for self-improvement.

    Breaks down accuracy, P&L, and confidence by different dimensions.

    Args:
        group_by: Group results by "symbol", "regime", "timeframe", or "direction"
    """
    return _fmt(_get("/agent/me/stats", {"group_by": group_by}))


@mcp.tool()
def get_signal_history(symbol: str, limit: int = 50) -> str:
    """Get historical signals for a symbol — useful for backtesting and pattern analysis.

    Returns recent signals with price, confidence, RSI, MACD, flow, and more.

    Args:
        symbol: The trading symbol (e.g., "BTC", "AAPL")
        limit: Max results 1-200 (default 50)
    """
    return _fmt(_get(f"/signals/history/{symbol.upper()}", {"limit": limit}))


@mcp.tool()
def get_predictions_archive(
    status: str = "all", symbol: str = "", regime: str = "",
    timeframe: str = "", limit: int = 500, offset: int = 0,
) -> str:
    """Query full prediction history from permanent archive (SQLite-backed).

    Unlike get_my_predictions (Redis, max 100), this returns unlimited history
    with P&L, regime, and resolution data — ideal for training and backtesting.

    Args:
        status: Filter by status — "all", "active", "hit", "missed"
        symbol: Filter by symbol (e.g., "BTC")
        regime: Filter by regime at prediction time
        timeframe: Filter by timeframe (e.g., "1h", "4h")
        limit: Max results 1-1000 (default 500)
        offset: Pagination offset
    """
    params = {"limit": limit, "offset": offset}
    if status != "all":
        params["status"] = status
    if symbol:
        params["symbol"] = symbol.upper()
    if regime:
        params["regime"] = regime
    if timeframe:
        params["timeframe"] = timeframe
    return _fmt(_get("/agent/me/predictions/archive", params))


@mcp.tool()
def get_stats_archive(group_by: str = "symbol") -> str:
    """Get full performance stats from permanent archive.

    Returns accuracy, P&L, and confidence breakdowns from all historical
    predictions (not just the last 100).

    Args:
        group_by: Group stats by "symbol", "regime", "timeframe", or "direction"
    """
    return _fmt(_get("/agent/me/stats/archive", {"group_by": group_by}))


@mcp.tool()
def get_signal_history_bulk(symbol: str, limit: int = 500, days: int = 0) -> str:
    """Get bulk historical signals from permanent archive — for backtesting.

    Returns signals with full indicator snapshots (RSI, MACD, Bollinger, VPIN,
    flow, etc.) from SQLite archive. Much larger history than the Redis-backed
    get_signal_history endpoint.

    Args:
        symbol: The trading symbol (e.g., "BTC", "AAPL")
        limit: Max results 1-5000 (default 500)
        days: Limit to last N days (0 = all time)
    """
    params = {"limit": limit}
    if days > 0:
        params["days"] = days
    return _fmt(_get(f"/signals/history/{symbol.upper()}/bulk", params))


@mcp.tool()
def register_webhook(url: str, secret: str = "", events: str = "prediction_resolved") -> str:
    """Register a webhook to receive prediction resolution notifications.

    When your predictions are resolved (hit or missed), TinkClaw will POST
    a JSON payload to your URL with HMAC-SHA256 signature if secret is set.

    Args:
        url: HTTPS callback URL to receive webhook POSTs
        secret: Optional HMAC secret for signature verification
        events: Comma-separated event types (default: "prediction_resolved")
    """
    body = {"url": url, "events": events}
    if secret:
        body["secret"] = secret
    return _fmt(_post("/agent/webhook", body))


@mcp.tool()
def get_webhook() -> str:
    """Check your current webhook registration status."""
    return _fmt(_get("/agent/webhook"))


@mcp.tool()
def delete_webhook() -> str:
    """Remove your webhook registration."""
    return _fmt(_delete("/agent/webhook"))


# ---------------------------------------------------------------------------
# Entrypoint
# ---------------------------------------------------------------------------


def main():
    mcp.run()


if __name__ == "__main__":
    main()
