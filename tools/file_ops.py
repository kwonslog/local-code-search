from config import logger, MAX_FILE_SIZE
from utils.security import safe_join
from utils.errors import FileTooLargeError
from pathlib import Path
from server import mcp


def read_text_file(full_path: Path) -> str:
    """
    지정된 파일 경로의 텍스트 파일을 읽어 문자열로 반환합니다.

    Args:
        full_path (Path): 읽을 파일의 절대 경로.

    Returns:
        str: 파일의 전체 내용.

    Raises:
        FileTooLargeError: 파일 크기가 MAX_FILE_SIZE를 초과할 경우 발생합니다.
    """
    size = full_path.stat().st_size
    if size > MAX_FILE_SIZE:
        raise FileTooLargeError(str(full_path), size)
    with open(full_path, "r", encoding="utf-8") as f:
        return f.read()


@mcp.tool()
def read_file(path: str) -> str:
    """
    지정된 경로의 파일을 안전하게 읽어 내용을 반환합니다.
    내부적으로 read_text_file()을 호출합니다.

    Args:
        path (str): 읽을 파일의 상대 또는 절대 경로.

    Returns:
        str: 파일의 전체 내용.
    """
    logger.info(f"[read_file] {path}")
    full_path = safe_join(path, must_exist=True)
    content = read_text_file(full_path)
    logger.info(f"[read_file] {len(content)} chars read")
    return content


@mcp.tool()
def write_file(path: str, content: str) -> str:
    """
    지정된 경로에 문자열 데이터를 저장합니다.
    기존 파일이 존재하면 덮어씁니다.

    Args:
        path (str): 파일을 저장할 경로.
        content (str): 저장할 문자열 데이터.

    Returns:
        str: 성공 시 "ok" 문자열을 반환합니다.
    """
    logger.info(f"[write_file] {path}, {len(content)} chars")
    full_path = safe_join(path)
    full_path.parent.mkdir(parents=True, exist_ok=True)
    with open(full_path, "w", encoding="utf-8", newline="") as f:
        f.write(content)
    logger.info(f"[write_file] done")
    return "ok"


@mcp.tool()
def read_files(paths: list[str], ignore_errors: bool = True) -> dict[str, str]:
    """
    여러 파일을 한 번에 읽어서 {경로: 내용} 형태의 딕셔너리로 반환.

    Args:
        paths (list[str]): 읽을 파일 경로 리스트
        ignore_errors (bool): True면 실패한 파일을 건너뜀

    Returns:
        dict[str, str]: {경로: 내용} 형태
    """
    logger.info(f"[read_files] {len(paths)} files requested")
    results = {}

    for path in paths:
        try:
            full_path = safe_join(path, must_exist=True)
            size = full_path.stat().st_size
            if size > MAX_FILE_SIZE:
                raise FileTooLargeError(str(full_path), size)

            with open(full_path, "r", encoding="utf-8") as f:
                results[path] = f.read()

            logger.info(f"[read_files] read {path} ({len(results[path])} chars)")

        except Exception as e:
            msg = f"[read_files] failed {path}: {e}"
            if ignore_errors:
                logger.warning(msg)
                continue
            else:
                raise e

    logger.info(f"[read_files] done, {len(results)} files read successfully")
    return results
