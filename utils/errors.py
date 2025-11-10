# utils/errors_commented.py
#
# 이 모듈은 MCP 서버에서 발생하는 오류를 표준화하여 관리하기 위한 클래스들을 정의합니다.
# 각 오류는 코드(code)와 메시지(message)를 포함하며,
# 클라이언트-서버 간 통신 시 명확한 에러 전달을 위해 설계되었습니다.

class MCPError(Exception):
    """표준화된 MCP 오류의 기본 클래스입니다.
    모든 사용자 정의 MCP 예외는 이 클래스를 상속받습니다.

    Attributes:
        code (str): 오류 코드 (예: 'INVALID_PATH', 'FILE_TOO_LARGE')
        message (str): 오류 메시지
    """
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message


class FileTooLargeError(MCPError):
    """지정된 파일의 크기가 허용 한도를 초과했을 때 발생하는 예외.

    Args:
        path (str): 파일 경로
        size (int): 파일 크기 (바이트 단위)
    """
    def __init__(self, path: str, size: int):
        super().__init__("FILE_TOO_LARGE", f"File '{path}' is too large ({size} bytes)")


class InvalidPathError(MCPError):
    """잘못되었거나 접근이 제한된 경로에 접근하려 할 때 발생하는 예외.

    Args:
        path (str): 문제가 된 파일 또는 디렉터리 경로
    """
    def __init__(self, path: str):
        super().__init__("INVALID_PATH", f"Invalid or restricted path: {path}")