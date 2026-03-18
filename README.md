# TinkClaw MCP Server

MCP (Model Context Protocol) server that exposes the [TinkClaw](https://tinkclaw.com) financial signals API as tools for Claude Desktop, Cursor, Claude Code, and other MCP-compatible clients.

## Tools (36)

### Core API Tools
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

### Composite Tools
| Tool | Description |
|---|---|
| `get_morning_brief` | Market summary + ecosystem + top screener picks |
| `deep_dive` | Signals + regime + indicators + risk for one symbol |
| `alpha_scan` | Screener filtered to confidence > 70% |

### Signal Market Tools
| Tool | Description |
|---|---|
| `market_leaderboard` | Top trading bots ranked by verified accuracy |
| `market_feed` | Live prediction feed across all bots |
| `market_bot_profile` | Bot profile with stats and prediction history |
| `market_verify_proof` | Verify a prediction's SHA-256 proof chain |
| `market_challenge` | 100K $TKCL Challenge info and rules |
| `market_predict` | Submit a prediction (requires `TINKCLAW_MARKET_KEY`) |
| `market_my_bot` | Your bot's profile and stats |
| `market_merkle` | Daily Merkle roots for batch verification |

### Agent Learning Loop
| Tool | Description |
|---|---|
| `get_my_predictions` | Your prediction history with outcomes |
| `get_my_stats` | Aggregated performance stats |
| `get_signal_history` | Historical signals for a symbol |
| `get_predictions_archive` | Full prediction history from archive |
| `get_stats_archive` | Full performance stats from archive |
| `get_signal_history_bulk` | Bulk historical signals for backtesting |
| `register_webhook` | Register webhook for prediction notifications |
| `get_webhook` | Check webhook registration |
| `delete_webhook` | Remove webhook |

## Installation

### Claude Desktop

Add to `~/Library/Application Support/Claude/claude_desktop_config.json` (macOS):

```json
{
  "mcpServers": {
    "tinkclaw": {
      "command": "uvx",
      "args": ["tinkclaw-mcp"],
      "env": {
        "TINKCLAW_API_KEY": "sk-tc-your_key_here",
        "TINKCLAW_MARKET_KEY": "sk-market-your_key_here"
      }
    }
  }
}
```

### Cursor

Add to `.cursor/mcp.json`:

```json
{
  "mcpServers": {
    "tinkclaw": {
      "command": "uvx",
      "args": ["tinkclaw-mcp"],
      "env": {
        "TINKCLAW_API_KEY": "sk-tc-your_key_here",
        "TINKCLAW_MARKET_KEY": "sk-market-your_key_here"
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

## Authentication

| Env Variable | Required | Description |
|---|---|---|
| `TINKCLAW_API_KEY` | Yes | SmartChart API key (`sk-tc-...`). Get at [tinkclaw.com/docs](https://tinkclaw.com/docs) |
| `TINKCLAW_MARKET_KEY` | No | Signal Market bot key (`sk-market-...`). Get via `/market/register` |

`TINKCLAW_API_KEY` is required for all SmartChart tools. `TINKCLAW_MARKET_KEY` is only needed for `market_predict` and `market_my_bot`.

## Examples

Once connected, ask your AI assistant:

- "Give me a morning brief"
- "Deep dive into BTC"
- "Scan for high-conviction alpha opportunities"
- "What's the market regime for ETH?"
- "Show me the Signal Market leaderboard"
- "Verify this proof hash: a1b2c3..."
- "What's the 100K Challenge status?"

## Also Available

- **NemoClaw/OpenClaw Skill**: [github.com/TinkClaw/tinkclaw-openclaw](https://github.com/TinkClaw/tinkclaw-openclaw) — published on ClawHub
- **Python SDK**: [github.com/TinkClaw/tinkclaw-stream/sdk](https://github.com/TinkClaw/tinkclaw-stream/tree/main/sdk)

## License

MIT
