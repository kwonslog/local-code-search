import os
from config import logger
from utils.security import safe_join
from server import mcp

@mcp.tool()
def get_metadata(path: str) -> dict:
    """
    파일의 메타데이터 반환.
    - 크기(size)
    - 생성일(ctime)
    - 수정일(mtime)
    - 접근권한(permission)
    """
    logger.info(f"[get_metadata] {path}")
    full_path = safe_join(path, must_exist=True)

    stat = full_path.stat()
    metadata = {
        "path": path,
        "size": stat.st_size,
        "created": stat.st_ctime,
        "modified": stat.st_mtime,
        "mode": oct(stat.st_mode & 0o777),
        "is_dir": full_path.is_dir(),
        "is_file": full_path.is_file(),
    }

    logger.info(f"[get_metadata] size={metadata['size']} bytes")
    return metadata
