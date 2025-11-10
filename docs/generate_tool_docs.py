import json
import inspect
from fastmcp import FastMCP
from pathlib import Path

def collect_tool_docs(output_path: str = "docs/tool_catalog.json"):
    mcp = FastMCP.get_instance()
    tools = mcp.tools  # 등록된 MCP 툴 목록
    result = []

    for name, fn in tools.items():
        doc = inspect.getdoc(fn) or "No description available."
        sig = str(inspect.signature(fn))
        result.append({
            "name": name,
            "signature": sig,
            "docstring": doc,
        })

    Path(output_path).write_text(json.dumps(result, ensure_ascii=False, indent=2))
    print(f"✅ Tool documentation written to {output_path}")

if __name__ == "__main__":
    collect_tool_docs()
