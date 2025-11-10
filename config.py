import os
import json
import logging
from pathlib import Path

# === 환경 변수 설정 ===
BASE_DIR = Path(os.getenv("MCP_BASE_DIR", r"C:\kwon\study\nextjs-project-architecture-template")).resolve()
MCP_PORT = int(os.getenv("MCP_PORT", 8000))
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()
MAX_FILE_SIZE = int(os.getenv("MAX_FILE_SIZE", 10 * 1024 * 1024))

# === 로깅(JSON 포맷) ===
class JSONFormatter(logging.Formatter):
    def format(self, record):
        data = {
            "time": self.formatTime(record, "%Y-%m-%dT%H:%M:%S"),
            "level": record.levelname,
            "message": record.getMessage(),
            "module": record.module,
        }
        return json.dumps(data, ensure_ascii=False)

logger = logging.getLogger("LocalMCP")
logger.setLevel(LOG_LEVEL)
handler = logging.StreamHandler()
handler.setFormatter(JSONFormatter())
logger.addHandler(handler)
