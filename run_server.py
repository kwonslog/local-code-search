import argparse
import threading
import time
from config import logger, MCP_PORT
from server import mcp
from start_ngrok import start_ngrok


def run_mcp_server():
    """
    FastMCP 서버를 구동하는 함수.
    """
    logger.info(f"Starting FastMCP server on 0.0.0.0:{MCP_PORT}")
    mcp.run(transport="http", host="0.0.0.0", port=MCP_PORT)


def main():
    # ────────────────────────────────────────────────
    # ① 명령행 인자 파싱
    # ────────────────────────────────────────────────
    parser = argparse.ArgumentParser(
        description="Run FastMCP local server (optionally with ngrok)."
    )
    parser.add_argument(
        "--mcp-only",
        action="store_true",
        help="Run only the MCP server without starting ngrok.",
    )
    parser.add_argument(
        "--port",
        type=int,
        default=MCP_PORT,
        help="Port to run the MCP server on (default from config.py).",
    )
    args = parser.parse_args()

    # ────────────────────────────────────────────────
    # ② MCP 서버 실행
    # ────────────────────────────────────────────────
    logger.info(
        "🚀 Launching FastMCP Server (%s mode)...",
        "MCP only" if args.mcp_only else "MCP + ngrok",
    )

    server_thread = threading.Thread(target=run_mcp_server, daemon=True)
    server_thread.start()

    # ────────────────────────────────────────────────
    # ③ ngrok 실행 (옵션)
    # ────────────────────────────────────────────────
    ngrok_process = None
    if not args.mcp_only:
        try:
            url, ngrok_process = start_ngrok()
            logger.info(f"🌍 Public URL: {url}/mcp")
            print("\n========================================")
            print("🚀 FastMCP Server with ngrok Running")
            print(f"🌍 Public URL: {url}/mcp")
            print(f"📡 Local Inspect URL: http://localhost:4040")
            print("========================================\n")
        except Exception as e:
            logger.error(f"❌ Failed to start ngrok: {e}")
    else:
        logger.info("🧩 Running MCP server only (no ngrok tunnel).")
        print("\n========================================")
        print("🚀 FastMCP Server Running (MCP-only mode)")
        print(f"📡 Local URL: http://localhost:{args.port}/mcp")
        print("========================================\n")

    # ────────────────────────────────────────────────
    # ④ 종료 처리
    # ────────────────────────────────────────────────
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🧹 Shutting down FastMCP server...")
        if ngrok_process:
            ngrok_process.terminate()
        exit(0)


if __name__ == "__main__":
    main()
