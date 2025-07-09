import os
import streamlit as st
from dotenv import load_dotenv
from openai import AzureOpenAI
import pandas as pd
from io import BytesIO
import re
import json
from datetime import datetime

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

# Streamlit 페이지 설정
st.set_page_config(page_title="테스트 도우미", page_icon="🧪")

# 사이드바 메뉴
menu = st.sidebar.radio("📂 기능 선택", ["🧪 테스트 케이스 생성기", "🐍 테스트 코드 생성기"])

# 공통 함수
def extract_table_to_dataframe(text: str) -> pd.DataFrame:
    lines = [line.strip() for line in text.splitlines() if '|' in line]
    if not lines or len(lines) < 2:
        return None
    table = [list(map(str.strip, line.strip('|').split('|'))) for line in lines]
    header = table[0]
    rows = table[2:] if re.match(r'^[- ]+$', ''.join(table[1])) else table[1:]
    df = pd.DataFrame(rows, columns=header)
    return df

def get_excel_download_button(df: pd.DataFrame, filename="test_cases.xlsx"):
    buffer = BytesIO()
    with pd.ExcelWriter(buffer, engine="xlsxwriter") as writer:
        df.to_excel(writer, index=False, sheet_name="TestCases")
    buffer.seek(0)
    st.download_button(
        label="📥 테스트 케이스 엑셀 다운로드",
        data=buffer,
        file_name=filename,
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )

# ---------------------------------------------
# 🧪 테스트 케이스 생성기
# ---------------------------------------------
if menu == "🧪 테스트 케이스 생성기":
    st.title("🧪 RAG 기반 테스트 케이스 생성기")

    if "messages" not in st.session_state:
        st.session_state.messages = [
            {
                "role": "system",
                "content": (
                    "당신은 테스트 케이스 전문가입니다. 사용자의 요청에 맞게 "
                    "명확하고 구조화된 테스트 케이스를 엑셀 형식으로 답변을 제공합니다. "
                )
            }
        ]

    # 대화 이력 표시
    for msg in st.session_state.messages:
        if msg["role"] == "user":
            st.chat_message("user").markdown(msg["content"])
        elif msg["role"] == "assistant":
            st.chat_message("assistant").markdown(msg["content"])

    # 사용자 입력 처리
    if user_input := st.chat_input("질문 또는 테스트 케이스 요청을 입력하세요"):
        st.chat_message("user").markdown(user_input)
        st.session_state.messages.append({"role": "user", "content": user_input})

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
            response = chat_client.chat.completions.create(
                model=chat_deployment_name,
                messages=st.session_state.messages,
                extra_body=rag_params
            )
            reply = response.choices[0].message.content

            if "not found" in reply.lower() or "찾지 못했습니다" in reply.lower():
                raise ValueError("Fallback triggered")

            st.chat_message("assistant").markdown(reply)
            st.session_state.messages.append({"role": "assistant", "content": reply})

            df = extract_table_to_dataframe(reply)
            if df is not None:
                get_excel_download_button(df)

        except Exception:
            fallback_response = chat_client.chat.completions.create(
                model=chat_deployment_name,
                messages=st.session_state.messages
            )
            fallback_reply = fallback_response.choices[0].message.content
            st.chat_message("assistant").markdown(fallback_reply)
            st.session_state.messages.append({"role": "assistant", "content": fallback_reply})

# ---------------------------------------------
# 🐍 테스트 코드 생성기 (엑셀 업로드 기반)
# ---------------------------------------------
elif menu == "🐍 테스트 코드 생성기":
    st.title("🐍 테스트 코드 생성기 (엑셀 기반)")

    uploaded_file = st.file_uploader("📄 테스트 케이스 엑셀 파일 업로드", type=["xlsx"])

    if uploaded_file:
        df = pd.read_excel(uploaded_file)
        st.success("✅ 엑셀 파일 업로드 완료")
        st.dataframe(df)

        code_prompt = f"""
다음은 테스트 케이스가 담긴 엑셀 표입니다. 이를 기반으로 Python 테스트 코드를 생성해주세요:

{df.to_markdown(index=False)}

- unittest 또는 pytest 스타일로 생성
- 함수 이름은 각 테스트 항목에 따라 자동 생성
"""

        response = chat_client.chat.completions.create(
            model=chat_deployment_name,
            messages=[
                {"role": "system", "content": "당신은 테스트 자동화 전문가입니다. 사용자가 제공한 테스트 케이스를 기반으로 Python 테스트 코드를 생성하세요."},
                {"role": "user", "content": code_prompt}
            ]
        )

        test_code = response.choices[0].message.content
        st.code(test_code, language="python")
