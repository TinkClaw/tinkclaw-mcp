# TinkClaw MCP Server

MCP (Model Context Protocol) server that exposes the [TinkClaw](https://tinkclaw.com) financial signals API as tools for Claude Desktop, Cursor, and other MCP-compatible clients.

## Tools

| Tool | Description |
|---|---|
| `get_signals` | Trading signals (BUY/SELL/HOLD) for a symbol |
| `get_signals_ml` | ML-enhanced signals for multiple symbols |
| `get_regime` | Market regime (trending/calm/volatile/crisis) |
| `get_confluence` | 6-layer confluence score |
| `get_indicators` | Technical indicators (RSI, MACD, Bollinger) |
| `get_risk_metrics` | Sharpe, VaR, Sortino, max drawdown |
| `get_correlation` | Correlation matrix between symbols |
| `get_screener` | All 60+ symbols ranked by signal strength |
| `get_ecosystem` | Cross-asset correlations + systemic risk |
| `get_order_flow` | Order flow data (Pro plan) |
| `get_news` | Financial news for a symbol |
| `get_market_summary` | Broad market overview |
| `get_backtest` | Strategy backtesting |
| `get_hurst_history` | Hurst exponent time series |
| `get_symbols` | List all supported symbols |
| `get_health` | API health check |
| **`get_morning_brief`** | Composite: market summary + ecosystem + top screener picks |
| **`deep_dive`** | Composite: signals + regime + indicators + risk for one symbol |
| **`alpha_scan`** | Composite: screener filtered to confidence > 70% |

## Installation

### Claude Desktop

Add to your Claude Desktop config (`~/Library/Application Support/Claude/claude_desktop_config.json` on macOS):

```json
{
  "mcpServers": {
    "tinkclaw": {
      "command": "uvx",
      "args": ["tinkclaw-mcp"],
      "env": {
        "TINKCLAW_API_KEY": "your_key_here"
      }
    }
  }
}
```

### Cursor

Add to Cursor's MCP settings (`.cursor/mcp.json`):

```json
{
  "mcpServers": {
    "tinkclaw": {
      "command": "uvx",
      "args": ["tinkclaw-mcp"],
      "env": {
        "TINKCLAW_API_KEY": "your_key_here"
      }
    }
  }
}
```

### Local development

```bash
cd tinkclaw-mcp
pip install -e .
TINKCLAW_API_KEY=your_key_here tinkclaw-mcp
```

Or run directly without installing:

```bash
TINKCLAW_API_KEY=your_key_here uvx tinkclaw-mcp
```

## Authentication

Set the `TINKCLAW_API_KEY` environment variable. Get your API key at [tinkclaw.com](https://tinkclaw.com).

## Examples

Once connected, ask Claude:

- "Give me a morning brief"
- "Deep dive into BTCUSD"
- "Scan for high-conviction alpha opportunities"
- "What's the market regime for ETHUSD?"
- "Show me risk metrics for AAPL and MSFT"
- "Run a hurst_momentum backtest on BTCUSD over 365 days"

## License

MIT
