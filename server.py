from config import logger, MCP_PORT
from mcp_instance import mcp

# MCP 툴 등록
import tools.file_ops
import tools.search_ops
import tools.tree_ops
import tools.analyze_ops
import tools.meta_ops
import tools.config_ops

# 모듈 내의 @mcp.tool() 데코레이터들이 자동 등록됨
# FastMCP는 import 시점에 데코레이터를 처리하므로, 별도 등록 불필요

if __name__ == "__main__":
    logger.info(f"Starting FastMCP server on 0.0.0.0:{MCP_PORT}")
    mcp.run(transport="http", host="0.0.0.0", port=MCP_PORT)
