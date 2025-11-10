from config import logger, MAX_FILE_SIZE, BASE_DIR
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
    for path in BASE_DIR.rglob("*"):
        if path.is_file() and query.lower() in path.name.lower():
            rel = path.relative_to(BASE_DIR).as_posix()
            results.append({
                "id": rel,
                "title": path.name,
                "url": f"file://{path}"
            })
    logger.info(f"[search] {len(results)} results")
    return {"results": results}

@mcp.tool()
def fetch(id: str) -> dict:
    """
    id(상대 경로)를 이용해 파일 내용을 가져옴.
    """
    logger.info(f"[fetch] {id}")
    full_path = safe_join(id, must_exist=True)

    size = full_path.stat().st_size
    if size > MAX_FILE_SIZE:
        raise FileTooLargeError(id, size)

    with open(full_path, "r", encoding="utf-8") as f:
        text = f.read()

    stat = full_path.stat()
    return {
        "id": id,
        "title": full_path.name,
        "text": text,
        "url": f"file://{full_path}",
        "metadata": {
            "size": stat.st_size,
            "modified": stat.st_mtime
        }
    }
