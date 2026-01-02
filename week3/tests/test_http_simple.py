import urllib.request
import urllib.error

def verify_server_simple():
    url = "http://127.0.0.1:8000/sse"
    print(f"📡 Connecting to {url} using urllib...")
    
    try:
        # Bypass proxies
        proxy_handler = urllib.request.ProxyHandler({})
        opener = urllib.request.build_opener(proxy_handler)
        
        req = urllib.request.Request(url, method="GET")
        with opener.open(req) as response:
            print(f"✅ Status Code: {response.getcode()}")
            print("Response Headers:", response.info())
    except urllib.error.HTTPError as e:
        print(f"⚠️ HTTP Error: {e.code} - {e.reason}")
    except urllib.error.URLError as e:
        print(f"❌ URL Error: {e.reason}")
    except Exception as e:
        print(f"❌ General Error: {e}")

if __name__ == "__main__":
    verify_server_simple()
