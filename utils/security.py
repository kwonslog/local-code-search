from pathlib import Path
from config import BASE_DIR

class AccessDeniedError(Exception):
    """루트 디렉토리 외부 접근 시 발생"""
    pass

def safe_join(relative_path: str, must_exist: bool = False) -> Path:
    """
    BASE_DIR 기준으로 안전한 전체 경로를 생성.
    - BASE_DIR 밖으로 벗어나는 경로 차단
    - 심볼릭 링크 접근 금지
    - 파일 존재 여부 확인 (옵션)
    """
    full_path = (BASE_DIR / relative_path).resolve()

    if not str(full_path).startswith(str(BASE_DIR)):
        raise AccessDeniedError(f"Access denied: {relative_path}")

    if full_path.is_symlink():
        raise AccessDeniedError(f"Symlink access not allowed: {relative_path}")

    if must_exist and not full_path.exists():
        raise FileNotFoundError(f"File not found: {relative_path}")

    return full_path
