# utils/security_commented.py
#
# 이 모듈은 MCP 서버의 파일 접근 보안을 담당합니다.
# 사용자가 요청한 경로가 BASE_DIR(서버 루트) 내부에만 존재하도록 강제하며,
# 심볼릭 링크나 디렉토리 탈출(../ 등)을 이용한 보안 우회를 차단합니다.

from pathlib import Path
from config import BASE_DIR


class AccessDeniedError(Exception):
    """
    루트 디렉토리(BASE_DIR) 외부 접근 시 발생하는 예외입니다.
    예를 들어, 사용자가 '../' 등의 경로로 상위 디렉토리에 접근하려고 할 때
    이를 탐지하여 즉시 차단합니다.
    """
    pass


# 안전한 경로 조합을 수행하는 핵심 함수
def safe_join(relative_path: str, must_exist: bool = False) -> Path:
    """
    BASE_DIR 기준으로 안전한 전체 경로를 생성합니다.

    Args:
        relative_path (str): BASE_DIR 내부의 상대 경로
        must_exist (bool): True일 경우, 경로가 실제 존재하지 않으면 예외 발생

    Returns:
        Path: 검증된 전체 경로 객체

    Raises:
        AccessDeniedError: BASE_DIR 밖의 경로나 심볼릭 링크 접근 시
        FileNotFoundError: must_exist=True이지만 파일이 존재하지 않을 때

    보안 로직:
        1. resolve()로 전체 절대 경로를 계산
        2. BASE_DIR 경로로 시작하지 않으면 접근 거부
        3. 심볼릭 링크 파일은 접근 차단
        4. 파일이 존재해야 하는 경우, 없으면 예외 발생
    """

    # 전체 경로 계산 및 정규화 (resolve는 '..' 등 상대 경로를 해석함)
    full_path = (BASE_DIR / relative_path).resolve()

    # 1️⃣ BASE_DIR 외부 접근 방지
    if not str(full_path).startswith(str(BASE_DIR)):
        raise AccessDeniedError(f"Access denied: {relative_path}")

    # 2️⃣ 심볼릭 링크 접근 차단
    if full_path.is_symlink():
        raise AccessDeniedError(f"Symlink access not allowed: {relative_path}")

    # 3️⃣ 존재 검증 옵션
    if must_exist and not full_path.exists():
        raise FileNotFoundError(f"File not found: {relative_path}")

    # 검증 통과 시 안전한 경로 반환
    return full_path
