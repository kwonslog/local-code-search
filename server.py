from fastmcp import FastMCP
from config import logger
from tools import file_ops, search_ops, tree_ops

mcp = FastMCP("Local File MCP")

# 모듈 내의 @mcp.tool() 데코레이터들이 자동 등록됨
# FastMCP는 import 시점에 데코레이터를 처리하므로, 별도 등록 불필요

if __name__ == "__main__":
    logger.info("Starting FastMCP server on 0.0.0.0:8000")
    mcp.run(transport="http", host="0.0.0.0", port=8000)
