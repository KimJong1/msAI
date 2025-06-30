# Azure OpenAI 기반 기능 테스트 케이스 생성기

이 프로젝트는 **Azure OpenAI의 LLM(대형 언어 모델)**을 활용하여  
Python 코드를 자동 분석하고, 해당 코드에 대한 **기능 테스트 케이스 목록**과  
각 테스트 항목에 대한 **예시 테스트 코드(Pytest 기반)**를 자동 생성하는 도구입니다.

## 주요 기능

- Python 함수/모듈 분석 및 기능 분해
- 핵심 기능별 테스트 항목 자동 추출
- `pytest` 기반 테스트 케이스 코드 자동 생성
- Streamlit UI 또는 CLI 환경 제공 예정

## 사용 사례

- 테스트 자동화가 필요한 개발자
- TDD(Test-Driven Development)를 빠르게 시작하고 싶은 팀
- 테스트 커버리지 확보가 필요한 레거시 코드 정리 작업

## 기술 스택

- Azure OpenAI (GPT)
- Python 3.11+
- pytest / pytest-mock
- Streamlit (옵션)

> 🚀 테스트 코드 작성을 LLM에게 맡기고, 더 중요한 로직 개발에 집중하세요!
