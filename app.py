import os
import streamlit as st
from openai import OpenAI

# =============================
# Page config
# =============================
st.set_page_config(
    page_title="Easy-Critic 듀얼 챗봇",
    page_icon="🧠",
    layout="centered",
)

MODEL_NAME = "gpt-5-mini"

APP_TITLE = "Easy-Critic: 친절한 해설과 냉철한 주석"
APP_DESC = (
    "한 번의 답변을 **두 층(Layer)** 으로 제공합니다.\n\n"
    "- **Layer 1 (Dr. Easy):** 선택한 눈높이에 맞춰 아주 쉽게 + 비유로 설명\n"
    "- **Layer 2 (Editorial Room):** 방금 설명의 단순화/생략/오해 가능성을 냉철하게 검증\n\n"
    "답변은 반드시 `---` 아래에서 **회색 배경의 비판적 검토**로 이어집니다."
)

PERSONAS = {
    "🐣 유치원생 모드 (비유 중심, 아주 쉽게)": (
        "말투는 아주 쉬운 어린이 눈높이. 짧은 문장. 비유를 많이. "
        "귀엽고 따뜻하게. 이모지 적극 사용."
    ),
    "🎓 대학생 족보 모드 (핵심 용어 중심, 명료하게)": (
        "대학생 시험 족보 느낌. 핵심 용어/정의/키포인트를 명료하게. "
        "불필요한 수사 줄이고, 구조화. 이모지는 적당히만."
    ),
    "👵 우리 할머니 모드 (구수하게, 옛날 이야기처럼)": (
        "구수한 할머니 말투. 옛날 이야기하듯 풀어주기. "
        "따뜻하고 생활 비유 중심. 이모지 적당히."
    ),
}

# =============================
# Session init
# =============================
def init_state():
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "persona" not in st.session_state:
        st.session_state.persona = list(PERSONAS.keys())[0]


def reset_chat():
    st.session_state.messages = []


init_state()

# =============================
# System prompt
# =============================
def build_system_prompt(persona_choice: str) -> str:
    persona_style = PERSONAS.get(persona_choice, PERSONAS[list(PERSONAS.keys())[0]])

    return f"""
너는 "Easy-Critic" 듀얼 챗봇이다.
사용자의 질문에 대해 반드시 **두 단계**로 답해야 한다.
절대로 한 단계만 출력하지 마라.

[1단계: The Friendly Explainer / Dr. Easy]
- 아래 페르소나 말투를 완벽히 연기한다:
  {persona_style}
- 반드시 포함:
  (a) 핵심 3줄 요약(각 1문장)
  (b) 찰떡 비유(Analogy) 1개
  (c) 이해 체크 질문 1개
- 이모지는 페르소나에 맞게 사용.

[2단계: The Editorial Room]
- 1단계가 끝나면 반드시 구분선 `---` 를 출력하고, 분위기를 180도 전환한다.
- 다음 3명의 가상 편집자가 1단계 설명을 비평한다(각 2~4줄):
  1) [Context Editor]: 생략된 전제/맥락을 최대 2줄로 보충
  2) [Skeptic]: 비유/요약이 낳을 수 있는 오해나 위험성을 구체적으로 경고
  3) [Meta-Critic]: 신뢰도 10점 만점 점수 + 한 줄 최종 코멘트
- 말투: 건조함, 분석적, 감정 배제.

[반드시 지켜야 할 출력 템플릿]
(Dr. Easy) 🧩
- 핵심 1:
- 핵심 2:
- 핵심 3:
비유: ...
체크 질문: ...

---
(Editorial Room) 🗞️
[Context Editor] ...
[Skeptic] ...
[Meta-Critic] 신뢰도: X/10 — ...
""".strip()


# =============================
# Rendering helper
# =============================
def render_easy_critic(text: str):
    if "---" not in text:
        st.markdown(text)
        st.warning("⚠️ 답변에 `---` 구분선이 없어요. 다시 질문하거나 프롬프트를 강화해야 할 수 있어요.")
        return

    top, bottom = text.split("---", 1)
    st.markdown(top.strip())

    st.markdown(
        f"""
<div style="
    background-color: rgba(128,128,128,0.18);
    border: 1px solid rgba(128,128,128,0.35);
    padding: 14px 14px;
    border-radius: 10px;
    white-space: pre-wrap;
    line-height: 1.55;
">
{bottom.strip()}
</div>
""",
        unsafe_allow_html=True,
    )


# =============================
# Sidebar
# =============================
with st.sidebar:
    st.header("⚙️ 설정")

    # ✅ 不再从环境变量自动回填，默认永远空
    api_key = st.text_input(
        "OpenAI API Key",
        type="password",
        value="",
        placeholder="sk-...",
        help="보안을 위해 자동으로 채우지 않습니다. 직접 붙여넣어 주세요.",
    )

    persona = st.selectbox(
        "설명 페르소나",
        list(PERSONAS.keys()),
        index=list(PERSONAS.keys()).index(st.session_state.persona),
    )
    st.session_state.persona = persona

    if st.button("🧹 대화 초기화", use_container_width=True):
        reset_chat()
        st.rerun()

    st.caption(f"모델: {MODEL_NAME}")


# =============================
# Main
# =============================
st.title(APP_TITLE)
st.write(APP_DESC)
st.divider()

if not api_key:
    st.info("왼쪽 사이드바에 OpenAI API Key를 입력하면 시작할 수 있어요.")
else:
    st.success("API Key 확인됨. 질문을 입력해봐요!")

# chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        if msg["role"] == "assistant":
            render_easy_critic(msg["content"])
        else:
            st.markdown(msg["content"])

user_text = st.chat_input("질문을 입력하세요. (예: '양자컴퓨터가 뭐야?' / 'DCF가 뭐야?')")

if user_text:
    st.session_state.messages.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    if not api_key:
        with st.chat_message("assistant"):
            st.warning("사이드바에 API Key를 먼저 입력해줘!")
    else:
        system_prompt = build_system_prompt(st.session_state.persona)
        client = OpenAI(api_key=api_key)

        with st.chat_message("assistant"):
            placeholder = st.empty()
            running = ""

            try:
                stream = client.responses.create(
                    model=MODEL_NAME,
                    instructions=system_prompt,
                    input=st.session_state.messages,
                    stream=True,
                )

                for event in stream:
                    etype = event.get("type") if isinstance(event, dict) else getattr(event, "type", None)
                    if etype == "response.output_text.delta":
                        delta = event.get("delta") if isinstance(event, dict) else getattr(event, "delta", "")
                        if delta:
                            running += delta
                            with placeholder.container():
                                render_easy_critic(running)

                    elif etype == "response.refusal.delta":
                        delta = event.get("delta") if isinstance(event, dict) else getattr(event, "delta", "")
                        if delta:
                            running += delta
                            with placeholder.container():
                                render_easy_critic(running)

                final_answer = running.strip() or "(빈 응답) 질문을 조금 더 구체적으로 해볼래요?"
            except Exception as e:
                final_answer = f"에러가 발생했어요: {e}"

            with placeholder.container():
                render_easy_critic(final_answer)

        st.session_state.messages.append({"role": "assistant", "content": final_answer})
