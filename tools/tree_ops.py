from config import logger, BASE_DIR
from utils.security import safe_join
from pathlib import Path
from functools import lru_cache
import time
from mcp_instance import mcp


def _build_tree(p: Path) -> dict:
    """
    주어진 경로(p)를 재귀적으로 순회하며 디렉터리 트리를 생성.
    파일이면 {"type": "file", "name": 파일명}
    디렉터리면 {"type": "directory", "name": 폴더명, "children": [...]}
    """
    if p.is_file():
        return {"type": "file", "name": p.name}
    children = []
    for c in sorted(p.iterdir()):
        try:
            children.append(_build_tree(c))
        except PermissionError:
            # 접근 불가한 디렉터리는 건너뛴다
            logger.warning(f"[list_dir_tree] Skipped permission-denied path: {c}")
            continue
    return {"type": "directory", "name": p.name, "children": children}


@lru_cache(maxsize=32)
def _cached_tree(path_str: str, minute_key: int) -> dict:
    """
    1분 단위로 캐싱되는 디렉터리 트리 빌드 함수.
    동일한 경로에 대한 반복 호출 성능 향상.
    """
    base_path = safe_join(path_str, must_exist=True)
    return _build_tree(base_path)


@mcp.tool()
def list_dir_tree(path: str | None = None) -> dict:
    """
    지정된 경로(path)의 디렉터리 트리를 JSON 형태로 반환.
    - path가 없을 경우 BASE_DIR을 기본 경로로 사용.
    - 대규모 디렉터리에서 성능 향상을 위해 1분 단위로 캐싱됨.
    """
    target_path = path or str(BASE_DIR)
    logger.info(f"[list_dir_tree] target={target_path}")

    minute_key = int(time.time() // 60)  # 캐시 무효화 기준 (1분 단위)
    tree = _cached_tree(target_path, minute_key)

    logger.info(f"[list_dir_tree] built for {target_path}")
    return tree
