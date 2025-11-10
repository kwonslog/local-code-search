# 개요

이 프로젝트는 ChatGPT(PC 웹 버전)를 사용하여 코드를 작성하거나 분석 및 개선 작업을 할때
로컬에 있는 소스 코드 정보를 제공하기 위한 목적으로 만들어 졌다.

## 구현방법

[FastMCP](https://github.com/jlowin/fastmcp) 프레임워크를 사용한다.

> 현재 MCP 프로토콜에 대한 이해도가 낮기 때문에 해당 도구를 사용하여 개발을 편리하게 할 수 있다.

## 프로젝트 생성

프로젝트를 생성하기 전에 [python](https://www.python.org/downloads/)을 설치해야 한다.

1. 폴더 생성
   - `local-code-search` 폴더를 생성하고, `git init` 명령을 실행하여 소스 코드를 관리 할 수 있도록 초기 설정을 한다.
   - 현재 이 프로젝트 코드는 git 으로 관리되고 있으며 로컬 PC 로 다운받는 방법은 `git clone https://github.com/kwonslog/local-code-search.git` 이다.

2. python 가상환경(venv) 생성 및 활성화
   ```bash

   # 가상환경을 생성하고
   python -m venv venv

   # activate 를 실행하면 된다.
   venv\Scripts\activate
   ```

3. 서버 실행에 필요한 모듈 설치
   ```bash
   pip install -r requirements.txt
   ```

4. ngrok 설치
   - 로컬 PC 에서 MCP 서버를 실행하고 ngrok 를 이용하여 이 로컬 서버를 외부에서 접근 가능 하도록 한다.
   - 파일을 [다운로드](https://ngrok.com/download/windows?tab=download) 받는다.
     > 윈도우 11 환경인 경우 해당 파일을 바이러스로 취급하기 때문에 Window 보안 -> 바이러스 및 위협 방지 -> 보호 기록 으로 가서 허용 처리 하고 다시 다운로드 하면 된다.
   - ngrok.exe 파일을 적당한 위치에 두고, 시스템 환경 변수에서 Path 로 등록하여 어디서든 실행 가능하도록 설정한다.
   - ngrok 을 실행하기 위해서는 사용자 토큰을 등록해야 하는데 ngrok 홈페이지에서 로그인해서 [토큰값을 확인](https://dashboard.ngrok.com/get-started/your-authtoken)한다.
     ```bash
     ngrok config add-authtoken `ngrok 에서 제공하는 토큰값`
     ```
   - 위 과정을 실행해도 ngrok 정상 실행이 되지 않는다면 python 가상환경(venv) 상태의 cmd 창에서 ngrok 명령을 실행해 보자.

> ngrok 을 따로 설치하는 이유는 MCP 서버를 디버깅 할때 필요하기 때문이다.

## 실행 방법

| 명령                               | 설명                                   |
| ---------------------------------- | -------------------------------------- |
| `python run_server.py`             | MCP 서버 + ngrok 자동 실행 (기본 모드) |
| `python run_server.py --mcp-only`  | MCP 서버만 실행 (ngrok 미실행)         |
| `python run_server.py --port 9000` | MCP 서버를 9000번 포트에서 실행        |

## 환경 변수

.env 파일안에 정의 되어 있다.

## ngrok 상태 확인
- http://localhost:4040/inspect/http

## ChatGPT 커넥터 연결 과정

- 연결 과정에서 발생하는 요청과 응답값을 확인해 본다.
- ngrok 을 로컬 PC 에서 실행했다면 `http://localhost:4040/inspect/http` 화면을 통해 요청/응답값을 확인 할 수 있다.

## ChatGPT 커넥터 설정

> 커텍터를 추가하려면 유료 요금제(개인이면 Plus)에 가입해야 합니다.

- PC 웹으로 ChatGPT에 접속하고 좌측 하단 설정창으로 들어간다.
- `연동 앱 및 커넥터`를 선택하고 우측에 활성화된 앱 및 커넥터 `만들기` 를 선택한다.
- `이름`과 `설명`을 입력한다. 인증은 사용하지 않기 때문에 `인증없음`을 선택한다.
- MCP 서버 URL 항목에 ngrok 의 Forwarding url 정보와 /mcp 를 합쳐서 입력한다.
  - 예를 들어 
    - Forwarding url : https://8dc6a2abce95.ngrok-free.app
    - 최종 MCP 서버 URL : https://8dc6a2abce95.ngrok-free.app/mcp
- 모두 입력후 만들기 버튼을 누른다.

아래 내용들은 만들기 버튼을 눌렀을때 MCP 서버로 요청하는 순서를 정리하였다.

## 최초 커넥터와 MCP 서버간 통신

- 요청 endpoint 는 2가지를 사용한다.
  - POST /mcp 
  - GET /mcp

- 요청 header 는 아래 필수값들을 추가해야 한다.
   ```
   Accept: application/json, text/event-stream
   Content-Type: application/json
   Mcp-Protocol-Version	2025-06-18
   Mcp-Session-Id	ab00356446ac4005a39078c2b3cfa178
   ```
  - Mcp-Session-Id 값은 handshake 응답 헤더의 값을 사용해야 한다.
  - Mcp-Protocol-Version 값은 handshake 응답 바디의 protocolVersion 값을 사용하면 된다.

### 최초 handshake 요청

`커넥터 만들기`를 누르면 ngrok 을 통해 로컬 PC 의 MCP 서버로 요청이 발생한다.

- 요청 endpoint
   ```
   POST /mcp
   ```

- 요청 body
   ```json
   {
      "jsonrpc": "2.0",
      "method": "initialize",
      "id": 1,
      "params": {
         "protocolVersion": "2025-03-26",
         "capabilities": {},
         "clientInfo": {
               "name": "openai-mcp",
               "version": "1.0.0"
         }
      }
   }
   ```

그리고 동일한 요청이지만 `protocolVersion` 만 변경된 요청이 한번 더 발생 한다.

- 요청 body
   ```json
   {
      "jsonrpc": "2.0",
      "method": "initialize",
      "params": {
         "protocolVersion": "2025-06-18",
         "capabilities": {},
         "clientInfo": {
               "name": "openai-mcp",
               "version": "1.0.0"
         }
      },
      "id": 0
   }
   ```

#### initialize 요청의 의미는?

클라이언트(커넥터)가 지원하는 MCP 버전과 기능을 서버에 전달하고 서버가 이를 지원하는지 확인하는 과정이다.

#### protocolVersion 관련 요청이 2번 발생한 이유는?
- 첫번째 요청은 최소 지원 가능한 버전을 확인하는 절차로 보인다.
- 두번째 요청은 더 최신의 버전을 지원하는지 여부를 확인하는 절차로 보인다.

### 최초 handshake 응답
- 응답 body
   ```json
   {
      "jsonrpc": "2.0",
      "id": 0,
      "result": {
         "protocolVersion": "2025-06-18",
         "capabilities": {
               "experimental": {},
               "prompts": {
                  "listChanged": true
               },
               "resources": {
                  "subscribe": false,
                  "listChanged": true
               },
               "tools": {
                  "listChanged": true
               }
         },
         "serverInfo": {
               "name": "Local File MCP",
               "version": "2.13.0.2"
         }
      }
   }
   ```
- 응답 header
   ```
   헤더에 있는 mcp-session-id 값은 handshake 이후 요청 header 에 포함되어야 하며 없을 경우 error 를 리턴한다.

   mcp-session-id: ab00356446ac4005a39078c2b3cfa178
   ```

#### mcp-session-id 값은?

- 클라이언트(커넥터)와 MCP 서버간의 대화 상태를 유지하기 위해 서버가 발급하는 값이다.
- MCP 통신은 단순 요청/응답이 아니라 지속적인 세션을 유지해야 한다.

### SSE(Server Send Event) 연결

요청 header 에 프로토콜과 세션 id 값을 추가하여 MCP 서버로 SSE 연결을 요청한다.

- 요청 endpoint
   ```
   GET /mcp
   ```

- 응답 body
   ```
   :ping - 2025-11-10 06:29:50.979235+00:00
   :ping - 2025-11-10 06:29:35.964333+00:00
   :ping - 2025-11-10 06:29:20.958648+00:00
   :ping - 2025-11-10 06:29:05.954619+00:00
   :ping - 2025-11-10 06:28:50.944883+00:00
   :ping - 2025-11-10 06:28:35.928236+00:00
   ...
   ```
   - 15초 간격으로 ping 메세지가 출력되는 것을 확인 할 수 있다.

### SSE 연결 완료

클라이언트(커넥터)가 서버와 GET /mcp 를 통해 연결 이후 연결 완료 알림을 보낸다.

- 요청 endpoint
   ```
   POST /mcp
   ```

- 요청 body
   ```json
   {
      "method": "notifications/initialized",
      "jsonrpc": "2.0"
   }
   ```

- 요청에 대한 응답은 202(Accepted) 상태값을 리턴하고, 별도 body 는 없다.

### 등록된 도구 조회

이제 클라이언트(커넥터)는 MCP 서버가 제공하는 기능들이 무엇인지 조회 한다.

- 요청 endpoint
   ```
   POST /mcp
   ```

- 요청 body
   ```json
   {
      "method": "tools/list",
      "jsonrpc": "2.0",
      "id": 1
   }
   ```

- 응답 body
   ```json
   {
      "jsonrpc": "2.0",
      "id": 1,
      "result": {
         "tools": [
               {
                  "name": "read_file",
                  "inputSchema": {
                     "properties": {
                           "path": {
                              "type": "string"
                           }
                     },
                     "required": [
                           "path"
                     ],
                     "type": "object"
                  },
                  "outputSchema": {
                     "properties": {
                           "result": {
                              "type": "string"
                           }
                     },
                     "required": [
                           "result"
                     ],
                     "type": "object",
                     "x-fastmcp-wrap-result": true
                  },
                  "_meta": {
                     "_fastmcp": {
                           "tags": []
                     }
                  }
               },
               {
                  "name": "write_file",
                  "inputSchema": {
                     "properties": {
                           "path": {
                              "type": "string"
                           },
                           "content": {
                              "type": "string"
                           }
                     },
                     "required": [
                           "path",
                           "content"
                     ],
                     "type": "object"
                  },
                  "outputSchema": {
                     "properties": {
                           "result": {
                              "type": "string"
                           }
                     },
                     "required": [
                           "result"
                     ],
                     "type": "object",
                     "x-fastmcp-wrap-result": true
                  },
                  "_meta": {
                     "_fastmcp": {
                           "tags": []
                     }
                  }
               },
               {
                  "name": "search",
                  "description": "BASE_DIR 하위에서 query 문자열이 포함된 파일 검색.",
                  "inputSchema": {
                     "properties": {
                           "query": {
                              "type": "string"
                           }
                     },
                     "required": [
                           "query"
                     ],
                     "type": "object"
                  },
                  "outputSchema": {
                     "additionalProperties": true,
                     "type": "object"
                  },
                  "_meta": {
                     "_fastmcp": {
                           "tags": []
                     }
                  }
               },
               {
                  "name": "fetch",
                  "description": "id(상대 경로)를 이용해 파일 내용을 가져옴.",
                  "inputSchema": {
                     "properties": {
                           "id": {
                              "type": "string"
                           }
                     },
                     "required": [
                           "id"
                     ],
                     "type": "object"
                  },
                  "outputSchema": {
                     "additionalProperties": true,
                     "type": "object"
                  },
                  "_meta": {
                     "_fastmcp": {
                           "tags": []
                     }
                  }
               },
               {
                  "name": "list_dir_tree",
                  "description": "지정된 경로(path)의 디렉터리 트리를 JSON 형태로 반환.\n\nArgs:\n    path (str | None): 기준 디렉터리 경로. 지정되지 않으면 BASE_DIR 사용.\n    exclude (list[str] | None): 무시할 파일명/디렉터리명 패턴 리스트. 예: ['__pycache__', '*.pyc']\n\nReturns:\n    dict: 디렉터리 트리 구조.\n\nNotes:\n    - .gitignore 기반의 기본 제외 패턴 포함 (.vscode, .venv, __pycache__)\n    - 1분 단위 캐시 적용 (exclude 패턴 포함)\n    - 접근 불가 경로 및 제외된 경로는 트리에 포함되지 않음.",
                  "inputSchema": {
                     "properties": {
                           "path": {
                              "anyOf": [
                                 {
                                       "type": "string"
                                 },
                                 {
                                       "type": "null"
                                 }
                              ],
                              "default": null
                           },
                           "exclude": {
                              "anyOf": [
                                 {
                                       "items": {
                                          "type": "string"
                                       },
                                       "type": "array"
                                 },
                                 {
                                       "type": "null"
                                 }
                              ],
                              "default": null
                           }
                     },
                     "type": "object"
                  },
                  "outputSchema": {
                     "additionalProperties": true,
                     "type": "object"
                  },
                  "_meta": {
                     "_fastmcp": {
                           "tags": []
                     }
                  }
               },
               {
                  "name": "count_lines",
                  "description": "코드 파일의 총 줄 수, 주석 수, 빈 줄 수를 계산.\n언어 무관하며 단순 패턴 기반.",
                  "inputSchema": {
                     "properties": {
                           "path": {
                              "type": "string"
                           }
                     },
                     "required": [
                           "path"
                     ],
                     "type": "object"
                  },
                  "outputSchema": {
                     "additionalProperties": true,
                     "type": "object"
                  },
                  "_meta": {
                     "_fastmcp": {
                           "tags": []
                     }
                  }
               },
               {
                  "name": "get_metadata",
                  "description": "파일의 메타데이터 반환.\n- 크기(size)\n- 생성일(ctime)\n- 수정일(mtime)\n- 접근권한(permission)",
                  "inputSchema": {
                     "properties": {
                           "path": {
                              "type": "string"
                           }
                     },
                     "required": [
                           "path"
                     ],
                     "type": "object"
                  },
                  "outputSchema": {
                     "additionalProperties": true,
                     "type": "object"
                  },
                  "_meta": {
                     "_fastmcp": {
                           "tags": []
                     }
                  }
               }
         ]
      }
   }
   ```

- 응답값 중에서 중요한 항목들을 보면
  - name : 제공하는 기능의 이름
  - description : 이 기능이 어떠한 일을 수행하는지에 대한 설명
  - inputSchema : 기능 호출의 인자 타입
  - outputSchema : 기능 응답값의 인자 타입

- ChatGPT는 응답값을 벡터화 해서 저장을 하는데 name, description 을 정확하게 입력해 두면 도구를 더 똑똑하게 선택한다.  
  (description 값이 없어도 name 값으로 유추하여 도구를 사용함.)

### 도구 호출

아래 기능은 디렉토리 목록을 요청하고 결과를 반환한다.

- 요청 endpoint
   ```
   POST /mcp
   ```

- 요청 body
   ```json
   {
      "jsonrpc": "2.0",
      "id": 0,
      "method": "tools/call",
      "params": {
         "name": "list_dir_tree",
         "arguments": {}
      }
   }
   ```

- 응답 body
   ```json
   {
      "jsonrpc": "2.0",
      "id": 0,
      "result": {
         "content": [
               {
                  "type": "text",
                  "text": "{\"type\":\"directory\",\"name\":\"tools\",\"children\":[{\"type\":\"file\",\"name\":\"analyze_ops.py\"},{\"type\":\"file\",\"name\":\"file_ops.py\"},{\"type\":\"file\",\"name\":\"meta_ops.py\"},{\"type\":\"file\",\"name\":\"search_ops.py\"},{\"type\":\"file\",\"name\":\"tree_ops.py\"}]}"
               }
         ],
         "structuredContent": {
               "type": "directory",
               "name": "tools",
               "children": [
                  {
                     "type": "file",
                     "name": "analyze_ops.py"
                  },
                  {
                     "type": "file",
                     "name": "file_ops.py"
                  },
                  {
                     "type": "file",
                     "name": "meta_ops.py"
                  },
                  {
                     "type": "file",
                     "name": "search_ops.py"
                  },
                  {
                     "type": "file",
                     "name": "tree_ops.py"
                  }
               ]
         },
         "isError": false
      }
   }
   ```
   - structuredContent 항목은 FastMCP 프레임워크에서 자동으로 삽입하는 데이터이다.
   - 삽입하는 이유는 편의성 제공이다.

## MCP 도구 추가 후 커넥터 갱신 방법

- ChatGPT 설정에서 `연동 앱 및 커텍터` 선택
- 추가한 커텍터를 선택하고 `새로고침` 실행
- 만약 새로고침이 실패하면 `연결 해제` 후 다시 `연결하기` 실행
- 그리고 `새로 고침` 실행하면 MCP 서버와 다시 handshake 한다.
- 커넥터 액션 목록을 보면 추가된 액션(도구)을 확인 할 수 있다.

## 기타

### ngrok 현재 사용량 확인 방법
- https://dashboard.ngrok.com/usage 로그인 필요.