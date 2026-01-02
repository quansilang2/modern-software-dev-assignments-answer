import asyncio
import httpx
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("debug-steam")

async def fetch_steam():
    # Pivot to Steam Store Search for Indie (tag 492)
    url = "https://store.steampowered.com/search/results/"
    params = {
        "query": "",
        "start": 0,
        "count": 10,
        "dynamic_data": "",
        "sort_by": "_ASC",
        "snr": "1_7_7_7000_7",
        "filter": "topsellers",
        "tags": "492", # Indie
        "infinite": 1
    }
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/115.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.5",
        "Accept-Encoding": "gzip, deflate, br",
        "Referer": "https://steamspy.com/",
        "Connection": "keep-alive",
        "Upgrade-Insecure-Requests": "1",
        "Sec-Fetch-Dest": "document",
        "Sec-Fetch-Mode": "navigate",
        "Sec-Fetch-Site": "none",
        "Sec-Fetch-User": "?1"
    }
    
    print(f"Fetching {url} with params {params}")
    
    async with httpx.AsyncClient(follow_redirects=True) as client:
        try:
            response = await client.get(url, params=params, headers=headers, timeout=30.0)
            print(f"Status Code: {response.status_code}")
            response.raise_for_status()
            data = response.json()
            print("Successfully fetched data")
            # Print first 5 keys to verify structure
            print(f"Keys: {list(data.keys())[:5]}")
        except Exception as e:
            print(f"Error: {e}")
            import traceback
            traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(fetch_steam())
