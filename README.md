# 💬 RAG 기반 테스트 케이스 생성기

AI와 Azure Cognitive Search (RAG: Retrieval-Augmented Generation)를 활용하여 테스트 케이스를 자동으로 생성하고 관리할 수 있는 **Streamlit 기반 웹 애플리케이션**입니다.

---

## 📌 주요 기능

- ✅ **Azure OpenAI + Azure Cognitive Search 기반 RAG** 기술로 지식 기반 테스트 케이스 생성
- ✅ 사용자 질문에 따라 **표 형식 테스트 케이스** 및 **Python 테스트 코드** 자동 생성
- ✅ 직관적인 **Streamlit 인터페이스** 제공
- ✅ RAG 인덱스에 정보가 없을 경우에도 **대화 이력 기반 fallback 응답** 처리
- ✅ Azure Web App 서비스를 통한 배포

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

4. **로컬 실행**

```bash
streamlit run aiSearch.py

5. **웹 앱 실행**

``` azure portal을 통해 web app 사전 구성 필요

<img width="1050" height="287" alt="Image" src="https://github.com/user-attachments/assets/0e776e75-a01a-40d4-94eb-b8db96e4751c"/>


## 💬 사용 예시

```plaintext
"사용자 등록 기능에 대한 테스트 케이스를 생성해줘"
"전화번호 마스킹을 확인하는 테스트를 만들어줘"
"로그인 기능에 대해 unittest 기반 테스트 코드를 작성해줘"


> 💡 **Tip:** 보다 정확하고 일관된 응답을 원하신다면, 질문을 **영어로 입력하는 것**을 추천드립니다.

