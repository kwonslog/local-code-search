<!-- 출처 : https://github.com/jlowin/fastmcp?tab=readme-ov-file -->

# FastMCP 2.0: 표준 프레임워크(번역본)

FastMCP는 Python 기반 MCP 개발을 개척했으며, FastMCP 1.0은 2024년에 공식 MCP SDK에 통합되었다.

이제 FastMCP 2.0 — 기본 프로토콜 구현을 훨씬 넘어서는, 적극적으로 유지·보수되는 프로덕션용 프레임워크다. SDK가 핵심 기능을 제공한다면, FastMCP 2.0은 실서비스에 필요한 모든 것을 제공한다.
예를 들어 다음과 같은 기능들이 포함된다:
고급 MCP 패턴(서버 조합, 프록시, OpenAPI/FastAPI 생성, 도구 변환), 엔터프라이즈 인증(Google, GitHub, WorkOS, Azure, Auth0 등), 배포 도구, 테스트 유틸리티, 완전한 클라이언트 라이브러리 등.

프로덕션용 MCP 애플리케이션을 개발하려면 다음을 설치하라:

```
pip install fastmcp
```

FastMCP는 MCP 애플리케이션을 구축하기 위한 표준 프레임워크로, 아이디어에서 프로덕션까지 가장 빠른 길을 제공한다.

---

## MCP란?

Model Context Protocol(MCP)은 LLM(대형 언어 모델)에 **컨텍스트와 도구**를 표준화된 방식으로 제공하는 프로토콜이다.
FastMCP는 엔터프라이즈 인증, 배포 도구, 완전한 생태계를 갖춘 **프로덕션급 MCP 서버**를 간단히 구축할 수 있게 해준다.

---

## 예시: 서버 코드

```python
# server.py
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def add(a: int, b: int) -> int:
    """두 수를 더한다"""
    return a + b

if __name__ == "__main__":
    mcp.run()
```

로컬에서 서버 실행:

```
fastmcp run server.py
```

---

## 📚 문서

FastMCP의 전체 문서는 [gofastmcp.com](https://gofastmcp.com)에 있으며, 세부 가이드, API 참고 자료, 고급 패턴을 포함한다.
이 README는 고수준의 개요만 다룬다.

문서는 LLM이 쉽게 읽을 수 있는 `llms.txt` 형식으로도 제공된다.

* `llms.txt`: 모든 문서 페이지를 나열한 사이트맵
* `llms-full.txt`: 전체 문서 내용(단, LLM 컨텍스트 길이를 초과할 수 있음)

커뮤니티: 다른 FastMCP 개발자들과 교류하려면 Discord 서버에 참여하라.

---

# 목차

* FastMCP v2 🚀
* 📚 문서
* MCP란?
* FastMCP를 사용하는 이유
* 설치
* 핵심 개념
* FastMCP 서버
* 도구 (Tools)
* 리소스 & 템플릿
* 프롬프트
* 컨텍스트
* MCP 클라이언트
* 인증
* 엔터프라이즈 인증 (제로 구성)
* 배포
* 개발에서 프로덕션까지
* 고급 기능

  * 프록시 서버
  * MCP 서버 구성(Composition)
  * OpenAPI & FastAPI 생성
* 서버 실행
* 기여 가이드

  * 사전 준비
  * 설정
  * 단위 테스트
  * 정적 검사
  * Pull Request

---

## MCP란?

Model Context Protocol(MCP)은 LLM 애플리케이션이 데이터를 안전하고 표준화된 방식으로 사용할 수 있도록 서버를 구축하는 방법을 제공한다.
MCP는 흔히 **“AI용 USB-C 포트”**라고 불린다.
즉, LLM이 사용할 수 있는 자원들을 일관된 방법으로 연결해주는 인터페이스다.

MCP 서버는 다음을 할 수 있다:

* **리소스(Resources)**: 데이터를 노출 (GET 엔드포인트처럼 동작)
* **도구(Tools)**: 기능을 제공 (POST 엔드포인트처럼 동작)
* **프롬프트(Prompts)**: LLM 상호작용 템플릿 정의
* 기타 확장 기능들

FastMCP는 이러한 MCP 서버를 Python스럽게 만들고 관리하고 상호작용할 수 있게 해주는 고수준 인터페이스를 제공한다.

---

## FastMCP를 사용하는 이유

FastMCP는 복잡한 프로토콜 세부 사항을 모두 처리하므로 개발자는 핵심 기능 구현에만 집중할 수 있다.

* 🚀 **빠름**: 고수준 인터페이스로 코드량을 줄여 개발 속도 향상
* 🍀 **단순함**: 최소한의 보일러플레이트로 서버 구축
* 🐍 **파이썬스러움**: 자연스러운 Python API
* 🔍 **완전함**: 프로덕션 환경에 필요한 모든 것 포함 (엔터프라이즈 인증, 배포, 테스트, 클라이언트 등)

FastMCP는 아이디어에서 프로덕션까지 가장 짧은 길을 제공한다.
로컬, FastMCP Cloud, 또는 자체 인프라 어디서든 배포 가능하다.

---

## 설치

추천 설치 방법 (uv 사용):

```
uv pip install fastmcp
```

자세한 설치, SDK 업그레이드, 개발자 설정은 Installation Guide 참조.

**라이선스 관련 참고:**
FastMCP는 CLI 기능을 위해 Cyclopts에 의존한다.
Cyclopts v4는 `docutils`를 간접 의존하여 일부 조직에서 라이선스 검토가 필요할 수 있다.
문제가 될 경우 Cyclopts v5 알파 버전(`pip install "cyclopts>=5.0.0a1"`)을 설치하거나 안정화 버전을 기다리면 된다.

---

## 핵심 개념

### FastMCP 서버

MCP 애플리케이션의 중심 객체로, 도구, 리소스, 프롬프트를 보유하며 연결과 인증 설정을 관리한다.

```python
from fastmcp import FastMCP

mcp = FastMCP(name="MyAssistantServer")
```

---

### 도구 (Tools)

LLM이 실행할 수 있는 Python 함수를 노출한다. (동기/비동기 모두 가능)
타입 힌트와 docstring을 통해 자동으로 스키마를 생성한다.

```python
@mcp.tool
def multiply(a: float, b: float) -> float:
    """두 수를 곱한다"""
    return a * b
```

---

### 리소스 & 템플릿

리소스는 읽기 전용 데이터 소스를 노출한다(GET 요청과 유사).
URI 템플릿을 이용해 동적 데이터 접근도 가능하다.

```python
@mcp.resource("config://version")
def get_version(): 
    return "2.0.1"

@mcp.resource("users://{user_id}/profile")
def get_profile(user_id: int):
    return {"name": f"User {user_id}", "status": "active"}
```

---

### 프롬프트 (Prompts)

LLM 상호작용을 위한 재사용 가능한 메시지 템플릿.

```python
@mcp.prompt
def summarize_request(text: str) -> str:
    """요약 요청 프롬프트 생성"""
    return f"다음 텍스트를 요약해 주세요:\n\n{text}"
```

---

### 컨텍스트 (Context)

도구, 리소스, 프롬프트 내부에서 MCP 세션 기능에 접근할 수 있다.

기능:

* 로그 기록 (`ctx.info()`, `ctx.error()`)
* LLM 샘플 요청 (`ctx.sample()`)
* 리소스 접근 (`ctx.read_resource()`)
* 진행 상황 보고 (`ctx.report_progress()`)

예시:

```python
from fastmcp import FastMCP, Context

mcp = FastMCP("My MCP Server")

@mcp.tool
async def process_data(uri: str, ctx: Context):
    await ctx.info(f"{uri} 처리 중...")
    data = await ctx.read_resource(uri)
    summary = await ctx.sample(f"요약: {data.content[:500]}")
    return summary.text
```

---

### MCP 클라이언트

FastMCP 클라이언트를 사용해 MCP 서버와 상호작용할 수 있다.
다양한 전송 방식(STDIO, SSE, In-Memory)을 지원한다.

```python
from fastmcp import Client

async def main():
    async with Client("my_server.py") as client:
        tools = await client.list_tools()
        result = await client.call_tool("add", {"a": 5, "b": 3})
```

여러 서버에 동시에 연결할 수도 있다:

```python
config = {
    "mcpServers": {
        "weather": {"url": "https://weather-api.example.com/mcp"},
        "assistant": {"command": "python", "args": ["./assistant_server.py"]}
    }
}
```

---

### 인증 (Authentication)

FastMCP는 엔터프라이즈급 인증을 기본 제공한다.
지원되는 OAuth 제공자:

* Google
* GitHub
* Microsoft Azure
* Auth0
* WorkOS
* Descope
* JWT / Custom / API Keys

서버 보호 예시:

```python
from fastmcp.server.auth.providers.google import GoogleProvider

auth = GoogleProvider(client_id="...", client_secret="...", base_url="https://myserver.com")
mcp = FastMCP("Protected Server", auth=auth)
```

클라이언트 연결:

```python
async with Client("https://protected-server.com/mcp", auth="oauth") as client:
    result = await client.call_tool("protected_tool")
```

FastMCP 인증의 장점:

* 프로덕션급: 지속성 저장소, 토큰 갱신, 에러 처리 포함
* 제로 설정 OAuth: `auth="oauth"` 한 줄이면 자동 설정
* 엔터프라이즈 통합: WorkOS, Azure AD, Auth0 등
* 개발 친화적: 브라우저 자동 실행, 콜백 서버, 환경 변수 지원
* 고급 아키텍처: 완전한 OIDC 지원, Dynamic Client Registration(DCR), 프록시 패턴 기반 OAuth

---

### 배포 (Deployment)

FastMCP는 로컬 개발부터 글로벌 규모 배포까지 모두 지원한다.

* 개발:

  ```
  fastmcp run server.py
  ```

* 프로덕션(FastMCP Cloud):

  * HTTPS 자동
  * 인증 내장
  * 제로 설정
  * 개인 서버는 무료

* 셀프 호스팅:

  ```
  mcp.run(transport="http", host="0.0.0.0", port=8000)
  ```

---

### 고급 기능

#### 프록시 서버

다른 MCP 서버를 중계하는 프록시 서버 생성 가능 (`FastMCP.as_proxy()` 사용)

#### MCP 서버 조합

여러 FastMCP 인스턴스를 하나의 부모 서버에 마운트 가능 (`mcp.mount()` 또는 `mcp.import_server()`)

#### OpenAPI & FastAPI 변환

`FastMCP.from_openapi()` 또는 `FastMCP.from_fastapi()`로 기존 API를 MCP 서버로 자동 변환.

---

### 서버 실행

```python
from fastmcp import FastMCP

mcp = FastMCP("Demo 🚀")

@mcp.tool
def hello(name: str) -> str:
    return f"Hello, {name}!"

if __name__ == "__main__":
    mcp.run()
```

지원되는 전송 프로토콜:

* STDIO (기본)
* HTTP (웹 배포용)
* SSE (기존 SSE 클라이언트 호환)

---

### 기여 (Contributing)

#### 사전 준비

* Python 3.10 이상
* uv (환경 관리용)

#### 설정

```bash
git clone https://github.com/jlowin/fastmcp.git 
cd fastmcp
uv sync
source .venv/bin/activate
```

#### 단위 테스트

```bash
pytest
uv run pytest --cov=src --cov=examples --cov-report=html
```

#### 정적 검사

`prek` 도구를 사용한다.

```bash
uv run prek install
prek run --all-files
```

#### Pull Request 절차

1. 리포지토리 fork
2. 브랜치 생성
3. 변경 및 테스트 추가
4. 테스트 및 정적 검사 통과 확인
5. 커밋 후 PR 생성
6. 주요 변경 시 이슈/토론 먼저 제안

---