# start_ngrok.py
from pyngrok import ngrok, conf
from config import logger, MCP_PORT
import os

def start_ngrok():
    logger.info("🚀 Starting pyngrok tunnel...")

    # .env 또는 환경변수에서 ngrok 토큰 읽기
    token = os.getenv("NGROK_AUTHTOKEN")
    if token:
        conf.get_default().auth_token = token

    public_url = ngrok.connect(MCP_PORT, "http").public_url
    logger.info(f"✅ ngrok tunnel active: {public_url}")
    return public_url, None

# def start_ngrok():
#     """
#     ngrok을 백그라운드로 실행하고, 생성된 터널의 public URL을 반환.
#     ngrok이 설치되어 있어야 함.
#     """
#     logger.info("🚀 Starting ngrok tunnel...")
#     process = subprocess.Popen(["ngrok", "http", str(MCP_PORT)], stdout=subprocess.DEVNULL)
#     time.sleep(3)  # ngrok이 초기화될 시간을 확보

#     try:
#         tunnels = requests.get("http://127.0.0.1:4040/api/tunnels").json()
#         public_url = tunnels["tunnels"][0]["public_url"]
#         logger.info(f"✅ ngrok tunnel active: {public_url}")
#         return public_url, process
#     except Exception as e:
#         logger.error(f"Failed to get ngrok URL: {e}")
#         process.terminate()
#         raise

if __name__ == "__main__":
    url, _ = start_ngrok()
    print(f"\nMCP Endpoint: {url}/mcp\n")
