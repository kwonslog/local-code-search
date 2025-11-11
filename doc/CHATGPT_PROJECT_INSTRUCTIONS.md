<!--

이 문서는 FastMCP 를 이용하여 MCP 서버 개발을 위해 사용한 ChatGPT 프로젝트 지침이다.

-->


# 🧠 FastMCP 기반 MCP 서버 구축 프로젝트 지침서

## 1. 개요

이 프로젝트의 목적은 **Python 기반 FastMCP 프레임워크**를 사용해 **ChatGPT Model Context Protocol(MCP)** 명세를 준수하는 **로컬 MCP 서버**를 구현하는 것이다.

이 MCP 서버는 ChatGPT 웹 클라이언트의 **커넥터 기능**을 통해 연결되어, ChatGPT가 로컬 파일 시스템의 코드를 탐색·분석하고 수정할 수 있도록 한다.

서버는 로컬 환경에서 실행되며, **ngrok을 이용해 HTTPS 터널링을 구성**해 외부 ChatGPT 클라이언트에서 안전하게 접근할 수 있다.

---

## 2. 목표

1. MCP 서버는 지정된 **루트 디렉토리(예: `/workspace`)** 이하의 파일 및 디렉토리 정보를 ChatGPT에 제공한다.
2. ChatGPT는 MCP 프로토콜을 통해 서버가 제공하는 **리소스(Resource)** 와 **툴(Tool)** 을 호출해 코드 탐색, 분석, 리팩토링을 수행할 수 있다.
3. MCP 서버는 요청에 따라 파일 내용을 반환하거나, ChatGPT가 생성한 코드를 저장할 수 있다.
4. 보안을 위해 루트 디렉토리 외부 접근은 차단하며, 경로 검증 로직을 통해 안전성을 확보한다.

---

## 3. 기능 명세

### 3.1 디렉토리 및 파일 구조 리소스 제공

FastMCP의 `@mcp.resource` 데코레이터를 사용해 루트 디렉토리 구조를 JSON 형태로 반환한다.

예시:

```python
from fastmcp import MCP, resource
import os, json

mcp = MCP("local-files")

@resource("filetree")
def file_tree():
    def scan(path):
        dirs, files = [], []
        for entry in os.scandir(path):
            if entry.is_dir():
                dirs.append(entry.name)
            else:
                files.append(entry.name)
        return {"path": path, "dirs": dirs, "files": files}
    return json.dumps(scan("/workspace"))
```

ChatGPT는 MCP 클라이언트를 통해 `"filetree"` 리소스를 요청하여 구조를 가져온다.

---

### 3.2 파일 내용 조회 툴

```python
from fastmcp import tool

@tool()
def read_file(path: str) -> dict:
    if not path.startswith("/workspace"):
        raise ValueError("Access outside root directory is not allowed.")
    with open(path, "r", encoding="utf-8") as f:
        return {"path": path, "content": f.read()}
```

응답 예시:

```json
{
  "path": "/workspace/internal/model/player.go",
  "content": "package model\n\ntype Player struct {...}"
}
```

---

### 3.3 파일 작성/수정 툴

```python
@tool()
def write_file(path: str, content: str) -> str:
    if not path.startswith("/workspace"):
        raise ValueError("Access outside root directory is not allowed.")
    base, ext = os.path.splitext(path)
    n = 1
    new_path = path
    while os.path.exists(new_path):
        new_path = f"{base}_{n}{ext}"
        n += 1
    with open(new_path, "w", encoding="utf-8") as f:
        f.write(content)
    return f"File written: {new_path}"
```

---

## 4. 통신 및 실행 구조

FastMCP 서버는 JSON-RPC 기반으로 MCP 표준에 따라 동작한다.
HTTP, WebSocket, 또는 Server-Sent Events(SSE)를 이용해 통신하며, ngrok을 통해 외부에서 접근 가능하다.

실행 예시:

```bash
pip install fastmcp
python server.py
ngrok http 8000
```

이후 ChatGPT 설정에서 ngrok URL을 MCP 커넥터로 등록한다.

---

## 5. 보안 및 운영 정책

| 항목      | 설명                                           |
| --------- | ---------------------------------------------- |
| 접근 제한 | 루트 디렉토리 외부 접근 차단                   |
| 쓰기 권한 | 루트 디렉토리 이하만 허용                      |
| 인증      | 로컬 모드 기본, 필요 시 Bearer Token 인증 확장 |
| 로깅      | 모든 요청/응답 로깅 (FastMCP 미들웨어 활용)    |
| 연결 방식 | ngrok 기반 HTTPS 터널링 사용                   |

---

## 6. ChatGPT의 역할

1. MCP 명세 분석 및 FastMCP 서버 설계 보조
2. Python 코드 생성 및 리팩토링 지원
3. MCP 툴/리소스 등록 및 테스트
4. ngrok 연결, MCP 커넥터 등록 검증
5. 코드 주석, 자동 문서화, 테스트 스크립트 생성 지원