from config import logger
from utils.security import safe_join
from pathlib import Path
from fastmcp import FastMCP
from functools import lru_cache
import time

mcp = FastMCP.get_instance()

def _build_tree(p: Path) -> dict:
    if p.is_file():
        return {"type": "file", "name": p.name}
    children = [_build_tree(c) for c in sorted(p.iterdir())]
    return {"type": "directory", "name": p.name, "children": children}

@lru_cache(maxsize=32)
def _cached_tree(path_str: str, minute_key: int) -> dict:
    base_path = safe_join(path_str, must_exist=True)
    return _build_tree(base_path)

@mcp.tool()
def list_dir_tree(path: str = ".") -> dict:
    """
    주어진 경로(path)를 기준으로 디렉터리 트리를 재귀적으로 탐색.
    1분 단위로 결과 캐싱.
    """
    logger.info(f"[list_dir_tree] {path}")
    minute_key = int(time.time() // 60)
    tree = _cached_tree(path, minute_key)
    logger.info(f"[list_dir_tree] built for {path}")
    return tree
