import re
from config import logger, MAX_FILE_SIZE
from utils.security import safe_join
from utils.errors import FileTooLargeError
from server import mcp

@mcp.tool()
def count_lines(path: str) -> dict:
    """
    코드 파일의 총 줄 수, 주석 수, 빈 줄 수를 계산.
    언어 무관하며 단순 패턴 기반.
    """
    logger.info(f"[count_lines] {path}")
    full_path = safe_join(path, must_exist=True)

    size = full_path.stat().st_size
    if size > MAX_FILE_SIZE:
        raise FileTooLargeError(path, size)

    with open(full_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    total = len(lines)
    empty = sum(1 for l in lines if not l.strip())
    comments = sum(1 for l in lines if l.strip().startswith(("//", "#")))

    result = {
        "path": path,
        "total_lines": total,
        "comment_lines": comments,
        "empty_lines": empty,
        "code_lines": total - comments - empty,
    }

    logger.info(f"[count_lines] total={total}, code={result['code_lines']}")
    return result
