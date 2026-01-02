# Week 3: Build a Custom MCP Server

This directory contains the implementation for the Week 3 assignment: **Game Market Intelligence MCP Server**.

## Project Overview
The project implements a Model Context Protocol (MCP) server that aggregates game market data from:
1.  **Apple App Store** (Top Charts)
2.  **SteamSpy** (Indie Game Trends)

## Directory Structure
```
week3/
├── game_market_mcp/      # The MCP Server source code
│   ├── main.py           # Entry point and tool definitions
│   ├── utils.py          # HTTP client and caching logic
│   ├── pyproject.toml    # Dependencies
│   └── README.md         # Detailed server documentation
└── README.md             # This file
```

## Setup Instructions

1.  **Navigate to the project directory**:
    ```bash
    cd week3
    ```

2.  **Install Dependencies**:
    Recommended using `poetry` (standard Python dependency manager):
    ```bash
    # Install poetry if you haven't
    pip install poetry
    
    # Install project dependencies
    poetry install
    ```
    Or using standard pip:
    ```bash
    pip install mcp[cli] httpx uvicorn pydantic
    ```

3.  **Run the Server**:
    To inspect tools:
    ```bash
    # using poetry
    poetry run python game_market_mcp/main.py inspect
    
    # using pip/python directly
    python game_market_mcp/main.py inspect
    ```

## MCP Configuration (Claude Desktop)

Add the following to your `claude_desktop_config.json`:

```json
{
  "mcpServers": {
    "game-market": {
      "command": "poetry",
      "args": [
        "run",
        "python",
        "game_market_mcp/main.py"
      ],
      "cwd": "/absolute/path/to/your/repo/week3"
    }
  }
}
```

## Features Implemented
- [x] **2+ Tools**: `get_app_store_charts` and `get_steam_indie_trends`.
- [x] **Reliability**: Implemented in-memory caching in `utils.py` to handle rate limits.
- [x] **External APIs**: Integrated Apple RSS and SteamSpy.
- [x] **Project Structure**: Organized as a proper Python project with `pyproject.toml`.
