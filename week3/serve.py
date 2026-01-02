import sys
import os
import uvicorn

# Setup sys.path explicitly to allow imports to work
current_dir = os.path.dirname(os.path.abspath(__file__))
module_dir = os.path.join(current_dir, "game_market_mcp")
if module_dir not in sys.path:
    sys.path.insert(0, module_dir)

# Import the MCP instance
try:
    from main import mcp
except ImportError as e:
    print(f"Failed to import main: {e}")
    sys.exit(1)

if __name__ == "__main__":
    # Ensure API Key is set for this session
    if "MCP_API_KEY" not in os.environ:
        os.environ["MCP_API_KEY"] = "test-key"
        print("🔑 [DEMO] Auto-configured MCP_API_KEY='test-key'")

    print("🚀 Starting Game Market MCP Server on http://localhost:8000")
    print("📡 SSE Endpoint: http://localhost:8000/sse")
    
    # Run Uvicorn
    # mcp.sse_app is the ASGI application provided by FastMCP for HTTP transport
    uvicorn.run(mcp.sse_app, host="0.0.0.0", port=8000)
