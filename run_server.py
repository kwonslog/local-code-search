import threading
from config import logger, MCP_PORT
from server import mcp
from start_ngrok import start_ngrok

def run_mcp_server():
    """
    FastMCP 서버를 실행하는 쓰레드 함수.
    """
    logger.info(f"Starting FastMCP server on 0.0.0.0:{MCP_PORT}")
    mcp.run(transport="http", host="0.0.0.0", port=MCP_PORT)

if __name__ == "__main__":
    url, ngrok_process = start_ngrok()

    server_thread = threading.Thread(target=run_mcp_server, daemon=True)
    server_thread.start()

    print("\n========================================")
    print("🚀 FastMCP Server Running")
    print(f"🌍 Public URL: {url}/mcp")
    print("========================================\n")

    try:
        server_thread.join()
    except KeyboardInterrupt:
        print("\n🧹 Shutting down MCP server...")
        ngrok_process.terminate()
        exit(0)
