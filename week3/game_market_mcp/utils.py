import httpx
import time
from typing import Dict, Any, Optional
import logging

# Configure basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger("game-market-mcp")

# Simple in-memory cache: { "key": (timestamp, data) }
_CACHE: Dict[str, tuple[float, Any]] = {}

async def fetch_json(url: str, params: Optional[Dict[str, Any]] = None, headers: Optional[Dict[str, str]] = None, cache_ttl: int = 3600) -> Any:
    """
    Fetches JSON data from a URL with caching support.
    
    Args:
        url: Target URL
        params: Query parameters
        headers: Request headers
        cache_ttl: Cache time-to-live in seconds (default: 1 hour)
    """
    cache_key = f"{url}:{str(params)}"
    
    # Check cache
    if cache_key in _CACHE:
        timestamp, data = _CACHE[cache_key]
        if time.time() - timestamp < cache_ttl:
            logger.info(f"Cache hit for {url}")
            return data
    
    # Cache miss - fetch fresh data
    # Prepare headers with default User-Agent
    req_headers = {"User-Agent": "GameMarketMCP/1.0"}
    if headers:
        req_headers.update(headers)

    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            logger.info(f"Fetching {url}")
            response = await client.get(url, params=params, headers=req_headers, timeout=10.0)
            response.raise_for_status()
            data = response.json()
            
            # Update cache
            _CACHE[cache_key] = (time.time(), data)
            return data
        except httpx.HTTPError as e:
            logger.error(f"HTTP Error fetching {url}: {e}")
            raise
        except Exception as e:
            logger.error(f"Error fetching {url}: {e}")
            raise
