from config import logger, MAX_FILE_SIZE, get_base_dir
from utils.security import safe_join
from utils.errors import FileTooLargeError
from server import mcp

@mcp.tool()
def search(query: str) -> dict:
    """
    BASE_DIR 하위에서 query 문자열이 포함된 파일 검색.
    """
    logger.info(f"[search] {query}")
    results = []
    for path in get_base_dir().rglob("*"):
        if path.is_file() and query.lower() in path.name.lower():
            rel = path.relative_to(get_base_dir()).as_posix()
            results.append({
                "id": rel,
                "title": path.name,
                "url": f"file://{path}"
            })
    logger.info(f"[search] {len(results)} results")
    return {"results": results}