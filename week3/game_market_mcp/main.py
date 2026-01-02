from mcp.server.fastmcp import FastMCP
import logging
import os

# Initialize FastMCP Server
mcp = FastMCP("Game Market Intelligence")
logger = logging.getLogger("game-market-mcp")

from utils import fetch_json
from typing import List, Dict, Any

def verify_api_key():
    """
    Verifies that the correct API Key is provided in the environment.
    """
    # For now, we hardcode the expectation that MCP_API_KEY must be set in the server environment
    # to "authenticate" that the server is configured securely.
    # In a real scenario, we would check the incoming request headers gainst this value.
    key = os.environ.get("MCP_API_KEY")
    if not key:
        return False
    return True

@mcp.tool()
async def get_app_store_charts(country: str = "us", category: str = "top-paid", limit: int = 10) -> str:
    """
    Retrieves top charts from Apple App Store.
    
    Args:
        country: Two-letter country code (e.g., 'us', 'cn', 'jp', 'gb').
        category: Chart category (e.g., 'top-paid', 'top-free').
        limit: Number of apps to return (max 100).
    """
    if not verify_api_key():
         return "Error: Server Misconfiguration. MCP_API_KEY not set in environment."

    url = f"https://rss.applemarketingtools.com/api/v2/{country}/apps/{category}/{limit}/apps.json"
    try:
        data = await fetch_json(url)
        results = data.get("feed", {}).get("results", [])
        
        # Format as a readable list
        output = []
        for app in results:
            name = app.get("name")
            artist = app.get("artistName")
            url = app.get("url")
            output.append(f"- {name} by {artist} ({url})")
            
        return "\n".join(output) if output else "No results found."
    except Exception as e:
        logger.error(f"Failed to fetch App Store charts: {e}")
        return f"Error fetching App Store charts: {str(e)}"

@mcp.tool()
async def get_steam_indie_trends(limit: int = 10) -> str:
    """
    Retrieves trending Indie games from Steam Store (Top Sellers).
    
    Args:
        limit: Number of games to return (default 10).
    """
    if not verify_api_key():
         return "Error: Server Misconfiguration. MCP_API_KEY not set in environment."

    # Using Steam Store Search API as SteamSpy is blocking requests
    url = "https://store.steampowered.com/search/results/"
    params = {
        "query": "",
        "start": 0,
        "count": limit,
        "dynamic_data": "",
        "sort_by": "_ASC",
        "snr": "1_7_7_7000_7",
        "filter": "topsellers",
        "tags": "492", # Indie
        "infinite": 1
    }
    
    try:
        data = await fetch_json(url, params=params)
        html_content = data.get("results_html", "")
        
        if not html_content:
            return "No data received from Steam."

        # Simple Regex parsing to avoid adding BeautifulSoup dependency
        import re
        
        # Regex to find game rows
        # We look for <span class="title">...</span> and optionally price info
        # This is a bit brittle but avoids heavy deps for this simple task
        
        output = []
        
        # Split into likely game blocks (each is an <a> tag usually)
        game_blocks = html_content.split('</a>')
        
        for block in game_blocks:
            if len(output) >= limit:
                break
                
            if 'class="title"' not in block:
                continue
                
            # Extract Title
            title_match = re.search(r'<span class="title">(.*?)</span>', block)
            title = title_match.group(1) if title_match else "Unknown Title"
            
            # Extract Price (look for final price first)
            price_match = re.search(r'<div class="discount_final_price">([^<]+)</div>', block)
            if not price_match:
                 # Start price if no discount
                 price_match = re.search(r'<div class="search_price">([^<]+)</div>', block)
            
            price_raw = price_match.group(1) if price_match else "N/A"
            price = price_raw.strip()
            
            # Retrieve Link (optional, from previous context, but easy to reconstruct or skip)
            # For brevity, just listing Title and Price
            
            output.append(f"- {title} (Price: {price})")
            
        return "\n".join(output) if output else "No Indie games found."
            
    except Exception as e:
        logger.error(f"Failed to fetch Steam trends: {e}")
        return f"Error fetching Steam trends: {str(e)}"


if __name__ == "__main__":
    # Provides CLI access: python main.py run / inspect
    mcp.run()
