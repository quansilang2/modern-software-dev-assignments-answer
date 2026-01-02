# [FEATURE] Game Market Intelligence MCP Server

## Current Context
- **System**: We are building a Model Context Protocol (MCP) server as part of the CS146S Week 3 assignment.
- **Goal**: To provide an AI agent (like Claude or Antigravity) with real-time "Game Market Intelligence" by bridging external APIs.
- **Pain Points**: Current AI models cannot access real-time gathered data from App Stores or Steam Charts. This server bridges that gap.

## Requirements

### Functional Requirements
- **Tool 1 (Mobile)**: `get_app_store_charts` - Retrieve top paid/free apps from Apple App Store for specific countries.
- **Tool 2 (PC/Console)**: `get_steam_indie_trends` - Retrieve trending Indie games from SteamSpy.
- **Transport**: Must support HTTP (Remote) transport (for +5 points extra credit).
- **Authentication**: Must support API Key authentication (for +5 points extra credit).

### Non-Functional Requirements
- **Reliability**: Graceful handling of API timeouts and rate limits (using caching).
- **Security**: Basic API Key validation to prevent unauthorized access.
- **Observability**: Structured logs to `stderr` (to avoid interfering with STDIO if we switch modes, though this is HTTP).

## Design Decisions

### 1. Framework Selection
Will choose **FastMCP (mcp[cli])** because:
- It effectively abstracts the low-level JSON-RPC details.
- It provides Pythonic decorators (`@mcp.tool`) for defining capabilities.
- It has built-in support for both SSE (HTTP) and STDIO transports.

### 2. Authentication Strategy
Will implement **Custom Middleware / Dependency** because:
- We need to validate the `X-API-Key` header on HTTP requests.
- This satisfies the "Auth implemented correctly" requirement simply and effectively without complex OAuth flows.

## Technical Design

### 1. Core Components
```python
# week3/game-market-mcp/main.py
from mcp.server.fastmcp import FastMCP

# Initialize Server
mcp = FastMCP("Game Market Intelligence")

# Tool Definitions
@mcp.tool()
async def get_app_store_charts(country: str = "us", category: str = "top-paid") -> str:
    """Retrieves top charts from Apple functionality."""
    pass
```

### 2. Data Models
```python
# week3/game-market-mcp/models.py (Optional, or inline)
from pydantic import BaseModel

class AppMetadata(BaseModel):
    name: str
    price: str
    icon_url: str

class SteamGame(BaseModel):
    name: str
    average_owners: str
    ccu: int
```

### 3. Integration Points
- **Upstream API 1**: Apple RSS Feed Generator (`https://rss.applemarketingtools.com/api/v2/...`)
- **Upstream API 2**: SteamSpy API (`https://steamspy.com/api.php`)
- **Downstream Client**: Antigravity IDE / Claude Desktop via HTTP SSE.

### 4. Files Changes
- `week3/game-market-mcp/main.py`: Entry point and tool definitions.
- `week3/game-market-mcp/utils.py`: HTTP helpers and caching logic.
- `week3/game-market-mcp/pyproject.toml`: Dependency definitions.

## Implementation Plan

1. Phase 1: **Setup & Connectivity**
   - Initialize project structure.
   - Install dependencies (`mcp`, `httpx`).
   - Verify basic "Hello World" tool works in Antigravity.

2. Phase 2: **Tool Implementation**
   - Implement `get_app_store_charts` with integration to Apple RSS.
   - Implement `get_steam_indie_trends` with integration to SteamSpy.
   - Add in-memory caching to respected API rate limits.

3. Phase 3: **Production Readiness**
   - Implement API Key authentication middleware.
   - Add comprehensive docstrings.
   - Generate `README.md`.

## Testing Strategy

### Unit Tests
- **Mocking**: Use `respx` or `pytest-mock` to mock external HTTP calls to Apple and SteamSpy.
- **Coverage**: Verify that tools return valid JSON strings even when APIs are weird/empty.

### Integration Tests
- **Antigravity Verification**: Configure Antigravity to connect to the local server URL.
- **Manual Verification**: Run queries like "What is the top paid game in China right now?" and verify the result.

## Observability

### Logging
- Use standard `logging` library.
- **Key Events**: Server startup, Tool invocation, Upstream API errors.
- **Output**: `stderr` (Standard Error) to separate from protocol traffic.

## Future Considerations

### Potential Enhancements
- Add more granular Steam filters (e.g., specific tags other than Indie).
- Add historical price tracking using a persistent database.

### Known Limitations
- SteamSpy data is updated daily, not real-time.
- Local in-memory cache clears on server restart.

## Dependencies

### Development Dependencies
- `poetry` or `uv` for package management.
- `pytest`, `httpx`, `uvicorn`.

## Security Considerations
- **API Key**: The secret key will be loaded from a `.env` file (`MCP_API_KEY`).
- **Exposure**: The server binds to `localhost` by default to prevent external network access unless explicitly configured.

## Rollout Strategy
1. **Development**: Run locally with `uv run week3/game-market-mcp/main.py`.
2. **Testing**: Verify with Antigravity manually.
3. **Delivery**: Commit code and updated `week2` artifacts to the repo.
