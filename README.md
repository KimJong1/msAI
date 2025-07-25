# 💬 RAG 기반 테스트 케이스 생성기

AI와 Azure Cognitive Search (RAG: Retrieval-Augmented Generation)를 활용하여 테스트 케이스를 자동으로 생성하고 관리할 수 있는 **Streamlit 기반 웹 애플리케이션**입니다.

---


## 대상 사용자
- QA
- 테스트 매니저
- 개발자 등 테스트 케이스 작성 실무자

---

## 문제
- 서비스 별 관리되는 테스트 케이스 양식의 일관성 부족  
- 개발자가 놓친 테스트 케이스 존재 가능성  
- 전사 차원의 규제나 규칙이 적용되지 않는 경우 발생  

---

## 솔루션 개요
- Azure AI + Azure Search 기반 RAG 활용을 통해  
  통일화된 테스트 케이스 생성

  

## 📌 주요 기능

- ✅ **Azure OpenAI + Azure Cognitive Search 기반 RAG** 기술로 지식 기반 테스트 케이스 생성
- ✅ 사용자 질문에 따라 **표 형식 테스트 케이스** 및 **Python 테스트 코드** 자동 생성
- ✅ 직관적인 **Streamlit 인터페이스** 제공
- ✅ RAG 인덱스에 정보가 없을 경우에도 **대화 이력 기반 fallback 응답** 처리
- ✅ Azure Web App으로 배포 환경 구현
---

## 📎 사전 준비 사항

이 애플리케이션을 사용하기 전, 다음과 같은 Azure AI Studio 환경 구성이 필요합니다:

1. **AI Foundry Project 구성**
   - LLM 모델, Embedding 모델, 그리고 에이전트를 생성하세요.
   - 생성한 에이전트의 `Deployment Name`을 `.env`의 `CHAT_DEPLOYMENT_NAME`에 설정합니다.

2. **Blob Storage + AI Search 인덱스 준비**
   - 데이터 파일을 **Blob Storage에 업로드**합니다.
   - **AI Search**에서 해당 파일을 기반으로 인덱스를 생성하고, `.env`에 관련 정보(`SEARCH_INDEX_NAME` 등)를 등록하세요.

> ⚠️ Azure OpenAI 및 Cognitive Search 사용 권한이 사전에 활성화되어 있어야 합니다.

---

![제목 없음](https://github.com/user-attachments/assets/788340c3-8793-48f3-84af-d9ff59d084c3)



---

## ⚙️ 설치 방법

1. **레포지토리 클론**

```bash
git clone https://github.com/your-username/msAI.git
cd msAI

---

2. **Python 패키지 설치**

```bash
pip install -r requirements.txt

---

3. **환경변수 설정 (.env)**

```env
OPENAI_API_KEY=your-azure-openai-key
OPENAI_ENDPOINT=https://your-resource-name.openai.azure.com
CHAT_DEPLOYMENT_NAME=your-deployment-name
SEARCH_ENDPOINT=https://your-search-service.search.windows.net
SEARCH_API_KEY=your-search-api-key
SEARCH_INDEX_NAME=your-index-name

---

4. **실행**

```bash
streamlit run aiSearch.py


## 💬 사용 예시

```plaintext
"사용자 등록 기능에 대한 테스트 케이스를 생성해줘"
"전화번호 마스킹을 확인하는 테스트를 만들어줘"
"로그인 기능에 대해 unittest 기반 테스트 코드를 작성해줘"


> 💡 **Tip:** 보다 정확하고 일관된 응답을 원하신다면, 질문을 **영어로 입력하는 것**을 추천드립니다.

---
https://user11mvp-d0f3hceke3bjcya6.eastus2-01.azurewebsites.net/

