import os
import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI

# 환경 변수 로드
load_dotenv()

# API 설정
openai_api_key = os.getenv("OPENAI_API_KEY")
openai_endpoint = os.getenv("OPENAI_ENDPOINT")
chat_deployment_name = os.getenv("CHAT_DEPLOYMENT_NAME")
search_endpoint = os.getenv("SEARCH_ENDPOINT")
search_api_key = os.getenv("SEARCH_API_KEY")
search_index_name = os.getenv("SEARCH_INDEX_NAME")

# OpenAI 클라이언트 초기화
chat_client = AzureOpenAI(
    api_version="2024-12-01-preview",
    azure_endpoint=openai_endpoint,
    api_key=openai_api_key
)

# Streamlit UI 설정
st.set_page_config(page_title="💬 RAG 기반 테스트 케이스 생성기", page_icon="🧪")
st.title("💬 RAG 기반 테스트 케이스 생성기")

# 세션 상태 초기화
if "messages" not in st.session_state:
    st.session_state.messages = [
        {
            "role": "system",
            "content": (
                "당신은 테스트 케이스 전문가입니다. 사용자의 요청에 맞게 "
                "명확하고 구조화된 테스트 케이스와 관련된 답변을 제공합니다. "
                "필요하면 표 형식과 python 기반 테스트 코드도 생성하세요."
            )
        }
    ]

# 대화 히스토리 출력 (system 메시지는 표시하지 않음)
for msg in st.session_state.messages:
    if msg["role"] == "user":
        st.chat_message("user").markdown(msg["content"])
    elif msg["role"] == "assistant":
        st.chat_message("assistant").markdown(msg["content"])

# 사용자 입력 처리
if user_input := st.chat_input("질문 또는 테스트 케이스 요청을 입력하세요"):

    st.chat_message("user").markdown(user_input)
    st.session_state.messages.append({"role": "user", "content": user_input})

    # RAG 설정
    rag_params = {
        "data_sources": [
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": search_endpoint,
                    "index_name": search_index_name,
                    "authentication": {
                        "type": "api_key",
                        "key": search_api_key
                    }
                }
            }
        ]
    }

    try:
        # RAG 기반 응답 요청
        response = chat_client.chat.completions.create(
            model=chat_deployment_name,
            messages=st.session_state.messages,
            extra_body=rag_params
        )
        reply = response.choices[0].message.content
        st.chat_message("assistant").markdown(reply)
        st.session_state.messages.append({"role": "assistant", "content": reply})

        # fallback 조건 (RAG 실패시)
        if "not found" in reply.lower() or "찾지 못했습니다" in reply.lower():
            raise ValueError("Fallback triggered")

    except Exception:
        fallback_response = chat_client.chat.completions.create(
            model=chat_deployment_name,
            messages=st.session_state.messages
        )
        fallback_reply = fallback_response.choices[0].message.content
        st.chat_message("assistant").markdown(fallback_reply)
        st.session_state.messages.append({"role": "assistant", "content": fallback_reply})
