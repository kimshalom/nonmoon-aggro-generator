import streamlit as st
from groq import Groq

# 1. 안전한 방식으로 금고(Secrets)에서 API 키 가져오기
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 2. 웹앱 UI 타이틀 및 소개글
st.title("🔥 어그로 장인의 연구주제 변환기")
st.subheader("여러분의 지루한 연구주제를 '학계의 문제작'으로 바꿔드립니다.")

# 3. 사용자 입력 (연구주제)
user_input = st.text_input("원래 연구주제를 입력하세요:", placeholder="예: 대학원생과 지도교수의 상호작용과 지도 유형에 관한 연구")

# 4. [업데이트] 3가지 수위 선택 라디오 버튼
taste = st.radio(
    "도발 수위를 선택하세요 🌶️",
    [
        "순한맛 (지적인 팩트 폭행)", 
        "매운맛 (인터넷 밈과 킹받는 드립 범벅)", 
        "전문가맛 (실전 학술용! 선명한 문제의식과 리프레이밍)"
    ],
    index=0
)

# 선택된 맛에 따라 AI에게 줄 프롬프트 설정
if "순한맛" in taste:
    system_instruction = (
        "너는 학계의 고정관념을 부수는 도발적이고 매력적인 연구 제목 매니저야. "
        "사용자가 평범한 연구 주제를 주면, 학자들의 호기심과 분노(?)를 동시에 자극할 만한 자극적이고 트렌디한 제목 3가지를 제안해줘. "
        "반드시 한국어로 답변해줘. 비속어는 절대 쓰지 말고 지적인 도발이어야 해. "
        "CRITICAL: 제목 외에 '이 제목은~' 같은 설명, 서론, 인사말은 절대로 하지 마. 오직 제목 3개만 딱 출력해."
    )
elif "매운맛" in taste:
    system_instruction = (
        "너는 세상에서 가장 유머러스하고 킹받는 연구 제목 매니저야. "
        "사용자가 평범한 연구 주제를 주면, 요즈음 유행하는 인터넷 밈(Meme), 직장인/대학원생의 애환이 담긴 눈물나는 풍자, "
        "학회의 시선을 단숨에 사로잡을 유쾌하고 짜릿한 드립을 섞어서 제목 3가지를 제안해줘. "
        "절대로 욕설이나 비속어는 쓰지 마. 오직 고급 유머와 드립으로만 승부해줘! "
        "CRITICAL: 제목 외에 '이 제목은~' 같은 설명, 서론, 인사말은 절대로 하지 마. 오직 제목 3개만 딱 출력해."
    )
else:
    # 🌟 새롭게 추가된 전문가맛 렉처 프롬프트
    system_instruction = (
        "너는 대학원생과 연구자를 위한 연구주제 리프레이밍 전문가야. "
        "사용자가 입력한 평범한 연구주제를 학술적 타당성은 유지하되, 문제의식이 선명하고 도발적인 제목 3가지로 바꾼다. "
        "과장된 클릭베이트(Clickbait)는 철저히 피하고, 개념적 긴장, 기존 담론에 대한 비판, 연구대상의 재해석이 날카롭게 드러나도록 제목을 제안해줘. "
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
                        {"role": "user", "content": f"원래 주제: {user_input}"}
                    ]
                )
                
                # 결과 출력
                st.success("결과가 나왔습니다!")
                st.write(response.choices[0].message.content)
                
            except Exception as e:
                st.error(f"에러가 발생했습니다: {e}")
    else:
        st.warning("연구주제를 먼저 입력해주세요!")
