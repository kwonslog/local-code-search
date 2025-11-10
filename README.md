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

<del>
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
</del>

4. ngrok 설치
   - pyngrok 을 사용하기 때문에 별도 설치는 필요 없다.
   
## ngrok 상태 확인
- http://localhost:4040/inspect/http

