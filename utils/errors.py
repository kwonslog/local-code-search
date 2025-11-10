class MCPError(Exception):
    """표준화된 MCP 오류"""
    def __init__(self, code: str, message: str):
        super().__init__(message)
        self.code = code
        self.message = message

class FileTooLargeError(MCPError):
    def __init__(self, path: str, size: int):
        super().__init__("FILE_TOO_LARGE", f"File '{path}' is too large ({size} bytes)")

class InvalidPathError(MCPError):
    def __init__(self, path: str):
        super().__init__("INVALID_PATH", f"Invalid or restricted path: {path}")
