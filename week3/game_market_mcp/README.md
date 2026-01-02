# Game Market Intelligence MCP Server

A Model Context Protocol (MCP) server that provides real-time market intelligence for the gaming industry.

## Features
*   **App Store Charts**
*   **Steam Indie Trends**

## Tools
1.  `get_app_store_charts(country, category, limit)`
2.  `get_steam_indie_trends(limit)`

## Installation

```bash
# Using poetry (Recommended)
poetry install
```
Or standard pip:
```bash
pip install mcp[cli] httpx uvicorn pydantic
```

## Running the Server

### Inspect
```bash
# Using poetry
poetry run python week3/game_market_mcp/main.py inspect

# Using standard python
python week3/game_market_mcp/main.py inspect
```
