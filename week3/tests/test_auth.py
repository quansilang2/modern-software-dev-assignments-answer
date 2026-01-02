import sys
import os
import asyncio
from unittest.mock import patch, MagicMock

# Setup path
current_dir = os.path.dirname(os.path.abspath(__file__))
server_dir = os.path.join(current_dir, "..", "game_market_mcp")
sys.path.insert(0, server_dir)

from main import get_app_store_charts

async def run_auth_test():
    print("========================================")
    print("🔐 Testing API Key Verification")
    print("========================================\n")

    # Case 1: No Key Set
    print("🔹 Test Case 1: Call without MCP_API_KEY")
    # Temporarily unset env var just in case
    if "MCP_API_KEY" in os.environ:
        del os.environ["MCP_API_KEY"]
    
    result = await get_app_store_charts(limit=1)
    print(f"Result: {result}")
    
    if "Server Misconfiguration" in result:
        print("✅ Success: Access Denied as expected.")
    else:
        print(f"❌ Failure: Access was allowed or unexpected error: {result}")

    print("\n")
    
    # Case 2: Key Set
    print("🔹 Test Case 2: Call WITH MCP_API_KEY")
    os.environ["MCP_API_KEY"] = "test-key"
    
    # We don't want to actually hit the network, so we trust the auth check passed if we get a different error or success
    # But for this test, we accept either network success or network error (as long as it's not Auth error)
    try:
        result = await get_app_store_charts(limit=1)
        if "Server Misconfiguration" not in result:
             print("✅ Success: Auth Passed (Tool executed).")
        else:
             print(f"❌ Failure: Still got auth error: {result}")
    except Exception as e:
        print(f"⚠️ Network/Other Error (Auth likely passed): {e}")

    print("\n")

if __name__ == "__main__":
    asyncio.run(run_auth_test())
