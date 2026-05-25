import streamlit as st
from groq import Groq

# 1. 무료 Groq API 키 입력 (따옴표 필수!)
client = Groq(api_key="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")
# 키를 직접 적지 않고, Streamlit 금고 시스템에서 꺼내오도록 변경
import os
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 2. 웹앱 UI 타이틀
st.title("🔥 어그로 장인의 연구주제 변환기")
st.subheader("여러분의 지루한 연구주제를 '학계의 문제작'으로 바꿔드립니다.")

# 3. 사용자 입력 (연구주제)
user_input = st.text_input("원래 연구주제를 입력하세요:", placeholder="예: 대학원생과 지도교수의 상호작용과 지도 유형에 관한 연구")

# 4. [신규 기능] 도발 수위 (맛) 선택 라디오 버튼
taste = st.radio(
    "도발 수위를 선택하세요 🌶️",
    ["순한맛 (지적인 팩트 폭행)", "매운맛 (약간의 비속어와 필터링 없는 매운맛)"],
    index=0
)

# 선택된 맛에 따라 AI에게 줄 지침(프롬프트)을 다르게 세팅합니다.
if "순한맛" in taste:
    system_instruction = (
        "너는 학계의 고정관념을 부수는 도발적이고 매력적인 연구 제목 매니저야. "
        "사용자가 평범한 연구 주제를 주면, 학자들의 호기심과 분노(?)를 동시에 자극할 만한 자극적이고 트렌디한 제목 3가지를 제안해줘. "
        "반드시 한국어로 답변해줘. 단, 지나친 비속어는 피하고 지적인 도발이어야 해. "
        "CRITICAL: 제목 외에 '이 제목은~' 같은 설명, 서론, 인사말은 절대로 하지 마. 오직 제목 3개만 딱 출력해."
    )
else:
    system_instruction = (
        "너는 필터링이 없는 거칠고 도발적인 연구 제목 매니저야. "
        "사용자가 평범한 연구 주제를 주면, 인터넷 밈(Meme)이나 약간의 거친 비속어, 매운맛 표현을 섞어서 학계에 완전히 시비를 거는 파격적인 제목 3가지를 제안해줘. "
        "반드시 한국어로 답변해줘. "
        "CRITICAL: 제목 외에 '이 제목은~' 같은 설명, 서론, 인사말은 절대로 하지 마. 오직 제목 3개만 딱 출력해."
    )

# 5. 변환 버튼 및 로직
if st.button("도발적인 주제로 변환하기 🚀"):
    if user_input:
        with st.spinner("학계에 시비 거는 중..."):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile", 
                    messages=[
                        {"role": "system", "content": system_instruction},
                        {"role": f"user", "content": f"원래 주제: {user_input}"}
                    ]
                )
                
                # 결과 출력
                st.success("결과가 나왔습니다!")
                st.write(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"에러가 발생했습니다: {e}")
    else:
        st.warning("연구주제를 먼저 입력해주세요!")