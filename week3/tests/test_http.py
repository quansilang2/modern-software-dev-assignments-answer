import httpx
import asyncio

async def verify_server():
    print("📡 Connecting to http://localhost:8000/sse ...")
    async with httpx.AsyncClient() as client:
        try:
            # We just want to see if the endpoint exists. 
            # A GET request to /sse usually opens a stream. 
            # We'll just connect and check the status code, then disconnect.
            async with client.stream("GET", "http://127.0.0.1:8000/sse") as response:
                print(f"✅ Connection Status Code: {response.status_code}")
                if response.status_code == 200:
                    print("🎉 Success: Server is accepting SSE connections!")
                else:
                    print(f"⚠️ Unexpected status: {response.status_code}")
        except Exception as e:
            print(f"❌ Connection Failed: {e}")

if __name__ == "__main__":
    asyncio.run(verify_server())
