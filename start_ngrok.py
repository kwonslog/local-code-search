import subprocess
import json
import time
import requests
from config import logger, MCP_PORT

def start_ngrok():
    """
    ngrok을 백그라운드로 실행하고, 생성된 터널의 public URL을 반환.
    ngrok이 설치되어 있어야 함.
    """
    logger.info("🚀 Starting ngrok tunnel...")
    process = subprocess.Popen(["ngrok", "http", str(MCP_PORT)], stdout=subprocess.DEVNULL)
    time.sleep(3)  # ngrok이 초기화될 시간을 확보

    try:
        tunnels = requests.get("http://127.0.0.1:4040/api/tunnels").json()
        public_url = tunnels["tunnels"][0]["public_url"]
        logger.info(f"✅ ngrok tunnel active: {public_url}")
        return public_url, process
    except Exception as e:
        logger.error(f"Failed to get ngrok URL: {e}")
        process.terminate()
        raise

if __name__ == "__main__":
    url, _ = start_ngrok()
    print(f"\nMCP Endpoint: {url}/mcp\n")
