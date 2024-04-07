# FCONLINE-COACH-AGENT  :soccer: :technologist:

## Introduction

<!-- ![short_example](https://github.com/hskimim/fconline-coach-agent/assets/38967492/91502507-50a8-497e-b001-cba1189e5268) -->

<img src = "https://github.com/hskimim/fconline-coach-agent/assets/38967492/91502507-50a8-497e-b001-cba1189e5268" width="50%" height="50%">

좋아하는 팀이나 감독의 전술을 [FC Online](https://fconline.nexon.com/main/index) 에서 구현해보세요! FC 온라인 게임의 전략적 수치를 LLM Agent를 통해 조정할 수 있습니다.

인터넷과 인게임에 공개된 정보들을 사용하여 LLM 에게 fc-online 의 팀/개인 전술에 대한 정보를 prompt engineering 을 통해 알려주고, 이를 OpenAI 의 gpt-4가 갖고 있는 실제 축구 전술 관련 정보와 연결지어 유저가 구현하고 싶은 축구 전술을 인게임에서도 구현할 수 있게 해줍니다.

<details>
  <summary>Agent 구조</summary>

  ![diagram](https://github.com/hskimim/fconline-coach-agent/assets/38967492/6c4edb0c-3908-47fe-b4fa-6deffcd542c4)

</details>


## Features
- [X] 팀 전술
- [X] 개인 전술
- [X] 전술 관련 캐주얼 대화
- [ ] planning, memory 가 탑재된 대화 -> 계속된 대화를 통해 전술을 교정해나간다.
- [ ] 개별 선수를 포지션이 아닌 이름으로 호출 ex) 윙백을 오버래핑시켜! -> 아놀드를 오버래핑시켜!


## Requirements
- Linux, Mac OS, or WSL on Windows
- Python >= 3.11
- Poetry >= 1.8

## How to use

1. Install Dependencies

```bash
poetry install
```

2. OpenAI key
```
- `sample.env` 를 `.env` 로 변경
- `.env` 에 openai key 입력 `OPENAI_API_KEY = "sk-xxx"`
```

3. Run Gradio Web UI

```bash
bash run_demo.sh 
```
