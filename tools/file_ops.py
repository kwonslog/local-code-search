from config import logger, MAX_FILE_SIZE
from utils.security import safe_join
from utils.errors import FileTooLargeError
from pathlib import Path
from fastmcp import FastMCP

mcp = FastMCP.get_instance()

def read_text_file(full_path: Path) -> str:
    size = full_path.stat().st_size
    if size > MAX_FILE_SIZE:
        raise FileTooLargeError(str(full_path), size)
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()

@mcp.tool()
def read_file(path: str) -> str:
    logger.info(f"[read_file] {path}")
    full_path = safe_join(path, must_exist=True)
    content = read_text_file(full_path)
    logger.info(f"[read_file] {len(content)} chars read")
    return content

@mcp.tool()
def write_file(path: str, content: str) -> str:
    logger.info(f"[write_file] {path}, {len(content)} chars")
    full_path = safe_join(path)
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    logger.info(f"[write_file] done")
    return "ok"
