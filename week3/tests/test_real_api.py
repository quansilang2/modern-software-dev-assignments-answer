import sys
import os
import asyncio

# Ensure we can import from the game_market_mcp package
# We add week3/game_market_mcp to sys.path so 'import main' and internal 'import utils' work
current_dir = os.path.dirname(os.path.abspath(__file__))
server_dir = os.path.join(current_dir, "..", "game_market_mcp")
sys.path.insert(0, server_dir)

# Now we can import the tools from main
# Note: Since main.py uses 'from utils import...', adding server_dir to sys.path makes 'utils' resolvable
try:
    from main import get_app_store_charts, get_steam_indie_trends
except ImportError as e:
    print(f"Import Error: {e}")
    print(f"Current sys.path: {sys.path}")
    sys.exit(1)

# Set API Key for testing
os.environ["MCP_API_KEY"] = "test-key"

async def run_tests():
    print("========================================")
    print("🧪 Running Game Market MCP Integration Tests")
    print("========================================\n")

    # Test Case 1: Apple App Store (China / Top Paid)
    print("🔹 Test Case 1: Fetching Top 5 Paid iOS Games in China")
    print("Calling: get_app_store_charts(country='cn', category='top-paid', limit=5)")
    try:
        result = await get_app_store_charts(country="cn", category="top-paid", limit=5)
        print("-" * 40)
        print(result)
        print("-" * 40)
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n")

    # Test Case 2: Apple App Store (US / Top Free)
    print("🔹 Test Case 2: Fetching Top 3 Free iOS Games in US")
    print("Calling: get_app_store_charts(country='us', category='top-free', limit=3)")
    try:
        result = await get_app_store_charts(country="us", category="top-free", limit=3)
        print("-" * 40)
        print(result)
        print("-" * 40)
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n")

    # Test Case 3: Steam Indie Trends
    print("🔹 Test Case 3: Fetching Top 5 Trending Indie Games on Steam")
    print("Calling: get_steam_indie_trends(limit=5)")
    try:
        result = await get_steam_indie_trends(limit=5)
        print("-" * 40)
        print(result)
        print("-" * 40)
    except Exception as e:
        print(f"❌ Error: {e}")

    print("\n")
    print("✅ Tests Completed")

if __name__ == "__main__":
    asyncio.run(run_tests())
