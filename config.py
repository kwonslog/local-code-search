import os
import json
import logging
from pathlib import Path
from dotenv import load_dotenv, set_key

# === 환경 변수 설정 ===
ENV_FILE = '.env'
load_dotenv(ENV_FILE)

_base_dir = Path(os.getenv('MCP_BASE_DIR', r'C:\kwon')).resolve()
MCP_PORT = int(os.getenv('MCP_PORT', 8000))
LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()
MAX_FILE_SIZE = int(os.getenv('MAX_FILE_SIZE', 10 * 1024 * 1024))


def get_base_dir() -> Path:
    """현재 BASE_DIR 경로를 반환합니다."""
    return _base_dir


def set_base_dir(new_path: str, persist: bool = False) -> None:
    """
    MCP_BASE_DIR 경로를 런타임에 변경합니다.

    Args:
        new_path (str): 새 기준 경로.
        persist (bool): True면 .env 파일에도 반영하여 영구 저장.
    """
    global _base_dir
    new_path = Path(new_path).resolve()
    if not new_path.exists():
        raise FileNotFoundError(f'경로를 찾을 수 없습니다: {new_path}')

    _base_dir = new_path
    os.environ['MCP_BASE_DIR'] = str(_base_dir)

    if persist:
        set_key(ENV_FILE, 'MCP_BASE_DIR', str(_base_dir))


# === 로깅(JSON 포맷) ===
class JSONFormatter(logging.Formatter):
    def format(self, record):
        data = {
            'time': self.formatTime(record, '%Y-%m-%dT%H:%M:%S'),
            'level': record.levelname,
            'message': record.getMessage(),
            'module': record.module,
        }
        return json.dumps(data, ensure_ascii=False)


logger = logging.getLogger('LocalMCP')
logger.setLevel(LOG_LEVEL)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
