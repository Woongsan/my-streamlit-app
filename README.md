# Easy-Critic: 친절한 해설과 냉철한 검증

Easy-Critic은 하나의 질문에 대해  
**“아주 쉽게 이해할 수 있는 설명”**과  
**“그 설명을 다시 냉철하게 검증하는 주석”**을 동시에 제공하는  
이중 구조(Dual-layer) AI 챗봇입니다.

---

## 🎯 프로젝트 개요

- **과목 / 프로그램**: 연세대 AX 캠프 – 트랙 1 소그룹 챌린지
- **형태**: 개인 프로젝트
- **목표**:  
  복잡한 개념을 빠르게 이해하면서도  
  “너무 단순화되어 본질이 왜곡되는 문제”를 동시에 해결하는 학습용 AI 도구 설계

---

## 💡 핵심 컨셉 (Dual Layer)

### Layer 1 – Dr. Easy (Friendly Explainer)
- 사용자가 선택한 설명 페르소나에 맞춰 설명
  - 🐣 유치원생 모드: 비유 중심, 아주 쉽게
  - 🎓 대학생 모드: 핵심 개념 중심
  - 👵 할머니 모드: 구수한 이야기체
- 핵심 요약 + 직관적인 비유 + 이모지 사용

### Layer 2 – Editorial Room (Critical Review)
- Layer 1 설명이 가진:
  - 생략된 전제
  - 오해 가능성
  - 과도한 단순화
- 을 **비판적으로 검토**
- 세 명의 가상 편집자 관점 제공:
  - Context Editor
  - Skeptic
  - Meta-Critic (신뢰도 점수)

---

## 🧠 해결하고자 한 문제

> “쉽게 설명하면 정확도가 떨어지고,  
> 정확하게 설명하면 이해하기 어렵다.”

Easy-Critic은 이 두 극단 사이의 긴장을  
**의도적으로 드러내는 구조**를 통해  
사용자가 더 깊이 사고하도록 돕는 것을 목표로 합니다.

---

## 🛠️ 기술 스택

- **Frontend / App Framework**: Streamlit
- **LLM API**: OpenAI API (gpt-5-mini)
- **언어**: Python

---

## ▶️ 실행 방법

### 1. 패키지 설치
```bash
pip install -r requirements.txt
