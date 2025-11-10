import re
from config import logger, MAX_FILE_SIZE
from utils.security import safe_join
from utils.errors import FileTooLargeError
from server import mcp

@mcp.tool()
def analyze_imports(path: str) -> dict:
    """
    Go 소스 파일(.go) 내 import 경로를 분석하여 반환.
    - 표준 라이브러리(import "fmt") 제외
    - 상대/로컬 import 식별
    """
    logger.info(f"[analyze_imports] {path}")
    full_path = safe_join(path, must_exist=True)

    if not full_path.suffix.endswith(".go"):
        raise ValueError(f"Not a Go source file: {path}")

    size = full_path.stat().st_size
    if size > MAX_FILE_SIZE:
        raise FileTooLargeError(path, size)

    with open(full_path, "r", encoding="utf-8") as f:
        content = f.read()

    imports = re.findall(r'import\s+"([^"]+)"', content)
    local_imports = [i for i in imports if not re.match(r'^(fmt|os|io|net|encoding|strings|errors|time|log)', i)]

    result = {
        "path": path,
        "imports": imports,
        "local_imports": local_imports,
        "count": len(imports)
    }

    logger.info(f"[analyze_imports] {len(imports)} total imports found")
    return result


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
