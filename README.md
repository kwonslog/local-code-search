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