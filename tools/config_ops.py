from server import mcp
from config import get_base_dir, set_base_dir

@mcp.tool()
def get_current_base_dir() -> dict:
    """
    현재 MCP_BASE_DIR 경로를 반환합니다.

    Returns:
        dict: 현재 BASE_DIR 경로 정보.
    """
    return {"base_dir": str(get_base_dir())}


@mcp.tool()
def change_base_dir(new_path: str, persist: bool = False) -> dict:
    """
    MCP_BASE_DIR 경로를 런타임에 변경합니다.

    Args:
        new_path (str): 새 기준 경로.
        persist (bool): True면 .env 파일에도 반영하여 영구 저장.

    Returns:
        dict: 변경된 경로 정보.
    """
    set_base_dir(new_path, persist)
    return {"base_dir": str(get_base_dir()), "persisted": persist}
