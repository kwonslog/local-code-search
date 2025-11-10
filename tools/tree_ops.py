import os
from config import logger, BASE_DIR
from utils.security import safe_join
from pathlib import Path
from functools import lru_cache
from fnmatch import fnmatch
import time
from mcp_instance import mcp

# 환경변수에서 DEFAULT_EXCLUDE 패턴 불러오기
# 쉼표(,)로 구분된 문자열을 리스트로 변환
# 예: DEFAULT_EXCLUDE=".git,.vscode,node_modules"
DEFAULT_EXCLUDE = [
    item.strip() for item in os.getenv(
        "DEFAULT_EXCLUDE",
        ".git,.vscode,.next,node_modules,venv,__pycache__"
    ).split(",")
]


# 내부 재귀 함수: 디렉토리 트리 생성 (제외 규칙 적용)
def _build_tree(p: Path, exclude: list[str] | None = None) -> dict:
    """
    주어진 경로(p)를 재귀적으로 순회하며 디렉터리 트리를 생성.
    exclude 리스트에 지정된 패턴과 일치하는 항목은 건너뜀.
    파일이면 {"type": "file", "name": 파일명}
    디렉터리면 {"type": "directory", "name": 폴더명, "children": [...]}
    """
    if exclude and any(fnmatch(p.name, pattern) for pattern in exclude):
        logger.debug(f"[list_dir_tree] Skipped excluded path: {p}")
        return None

    if p.is_file():
        return {"type": "file", "name": p.name}

    children = []
    for c in sorted(p.iterdir()):
        try:
            node = _build_tree(c, exclude)
            if node:
                children.append(node)
        except PermissionError:
            logger.warning(f"[list_dir_tree] Skipped permission-denied path: {c}")
            continue

    return {"type": "directory", "name": p.name, "children": children}


@lru_cache(maxsize=32)
def _cached_tree(path_str: str, minute_key: int, exclude_key: str) -> dict:
    """
    1분 단위로 캐싱되는 디렉터리 트리 빌드 함수.
    exclude_key를 포함하여 캐시 무효화 기준을 세분화.
    """
    base_path = safe_join(path_str, must_exist=True)
    exclude_patterns = exclude_key.split(',') if exclude_key else None
    return _build_tree(base_path, exclude_patterns)


@mcp.tool()
def list_dir_tree(path: str | None = None, exclude: list[str] | None = None) -> dict:
    """
    지정된 경로(path)의 디렉터리 트리를 JSON 형태로 반환.

    Args:
        path (str | None): 기준 디렉터리 경로. 지정되지 않으면 BASE_DIR 사용.
        exclude (list[str] | None): 무시할 파일명/디렉터리명 패턴 리스트. 예: ['__pycache__', '*.pyc']

    Returns:
        dict: 디렉터리 트리 구조.

    Notes:
        - .gitignore 기반의 기본 제외 패턴 포함 (.vscode, .venv, __pycache__)
        - 1분 단위 캐시 적용 (exclude 패턴 포함)
        - 접근 불가 경로 및 제외된 경로는 트리에 포함되지 않음.
    """
    target_path = path or str(BASE_DIR)
    logger.info(f"[list_dir_tree] target={target_path}")

    # 사용자 정의 제외 리스트와 기본 제외 리스트 결합
    effective_exclude = sorted(set(DEFAULT_EXCLUDE + (exclude or [])))

    minute_key = int(time.time() // 60)
    exclude_key = ','.join(effective_exclude)

    tree = _cached_tree(target_path, minute_key, exclude_key)

    logger.info(f"[list_dir_tree] built for {target_path} (exclude={effective_exclude})")
    return tree
