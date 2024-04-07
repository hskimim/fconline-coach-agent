SEPERATOR = "=" * 20

MODEL_NM = "gpt-4-0125-preview"
LONG_MODEL_NM = "gpt-4-0125-preview"
TEMPERATURE: float = 0.0

ALL_POSITIONS = [
    "LS",
    "ST",
    "RS",
    "LW",
    "LF",
    "CF",
    "RF",
    "RW",
    "LAM",
    "CAM",
    "RAM",
    "LM",
    "LCM",
    "CM",
    "RCM",
    "RM",
    "LWB",
    "LDM",
    "CDM",
    "RDM",
    "RWB",
    "LB",
    "LCB",
    "SW",
    "RCB",
    "RB",
    "GK",
]


FORMATION_POSITION_MAPPER = {
    "4231": [
        "GK",
        "RB",
        "LCB",
        "RCB",
        "LB",
        "RDM",
        "LDM",
        "RAM",
        "LAM",
        "CAM",
        "ST",
    ],
    "343": ["GK", "LCB", "CB", "RCB", "LM", "LCM", "RCM", "RM", "LF", "RF", "ST"],
    "343(2)": ["GK", "LCB", "CB", "RCB", "LM", "LCM", "RCM", "RM", "LW", "RF", "SW"],
    "3412": ["GK", "LCB", "CB", "RCB", "LM", "LCM", "RCM", "RM", "CAM", "LS", "RS"],
    "3232": [
        "GK",
        "LCB",
        "CB",
        "RCB",
        "LDM",
        "RDM",
        "CM",
        "LM",
        "RM",
        "CF",
        "ST",
    ],
    "32212": ["GK", "LCB", "CB", "RCB", "LM", "LDM", "RDM", "RM", "CAM", "LS", "RS"],
    "31213": ["GK", "LCB", "CB", "RCB", "LM", "CDM", "RM", "CAM", "LW", "ST", "RW"],
    "3142": ["GK", "LCB", "CB", "RCB", "LM", "LCM", "CDM", "RCM", "RM", "LS", "RS"],
    "451": ["GK", "LB", "LCB", "RCB", "RB", "LM", "LCM", "CM", "RCM", "RM", "ST"],
    "442": ["GK", "LB", "LCB", "RCB", "RB", "LM", "LCM", "RCM", "RM", "CF", "ST"],
    "442(2)": ["GK", "LB", "LCB", "RCB", "RB", "LM", "LCM", "RCM", "RM", "LS", "RS"],
    "4411": ["GK", "LB", "LCB", "RCB", "RB", "LM", "LCM", "RCM", "RM", "CAM", "ST"],
    "433": ["GK", "LB", "LCB", "RCB", "RB", "LCM", "CM", "RCM", "LW", "ST", "RW"],
    "433(2)": ["GK", "LB", "LCB", "RCB", "RB", "LCM", "CM", "RCM", "LF", "ST", "RF"],
    "4321": ["GK", "LB", "LCB", "RCB", "RB", "LM", "CM", "RM", "LAM", "RAM", "ST"],
    "4312": ["GK", "LB", "LCB", "RCB", "RB", "LCM", "CM", "RCM", "CAM", "LS", "RS"],
    "424": ["GK", "LB", "LCB", "RCB", "RB", "LCM", "RCM", "LW", "RW", "LS", "RS"],
    "4222": ["GK", "LB", "LCB", "RCB", "RB", "LM", "LDM", "RDM", "RM", "LS", "RS"],
    "4222(2)": ["GK", "LB", "LCB", "RCB", "RB", "LAM", "LDM", "RDM", "RAM", "LS", "RS"],
    "42211": ["GK", "LB", "LCB", "RCB", "RB", "LM", "LDM", "RDM", "RM", "CAM", "ST"],
    "4213": ["GK", "LB", "LCB", "RCB", "RB", "LCM", "RCM", "CAM", "LW", "RW", "ST"],
    "4213(2)": ["GK", "LB", "LCB", "RCB", "RB", "LCM", "RCM", "CM", "LW", "RW", "ST"],
    "4141": ["GK", "LB", "LCB", "RCB", "RB", "LM", "LCM", "CDM", "RCM", "RM", "ST"],
    "4132": ["GK", "LB", "LCB", "RCB", "RB", "LM", "CDM", "CM", "RM", "LS", "RS"],
    "4123": ["GK", "LB", "LCB", "RCB", "RB", "LCM", "CDM", "RCM", "LW", "ST", "RW"],
    "4123(2)": ["GK", "LB", "LCB", "RCB", "RB", "LCM", "CDM", "RCM", "LW", "CF", "RW"],
    "41212": ["GK", "LB", "LCB", "RCB", "RB", "LM", "CDM", "RM", "CAM", "LS", "RS"],
    "41212(2)": [
        "GK",
        "LB",
        "LCB",
        "RCB",
        "RB",
        "LCM",
        "CDM",
        "RCM",
        "CAM",
        "LS",
        "RS",
    ],
    "541": ["GK", "LWB", "LCB", "CB", "RCB", "RWB", "LM", "LCM", "RCM", "RM", "ST"],
    "532": ["GK", "LWB", "LCB", "CB", "RCB", "RWB", "LCM", "CM", "RCM", "LS", "RS"],
    "523": ["GK", "LWB", "LCB", "CB", "RCB", "RWB", "LCM", "RCM", "LW", "ST", "RW"],
    "5212": ["GK", "LWB", "LCB", "CB", "RCB", "RWB", "LCM", "RCM", "CAM", "LS", "RS"],
    "51211": ["GK", "LWB", "LCB", "CB", "RCB", "RWB", "LM", "CDM", "RM", "CAM", "ST"],
}

INVALID_CURRENT_TACTIC_ERR: str = """
전술값의 format을 제가 이해할 수 없는 형태입니다. 아래의 예시 format을 따라 넣어주세요.
```json[
{"포메이션": "4-3-3"},
{"수비 스타일": "공 뺏긴 직후 압박"},
{"빌드업 플레이": "느린 빌드업"},
{"수비 포지셔닝": {"폭": 5, "깊이": 5}},
{"공격 포지셔닝": {"폭": 8, "박스 안 쪽 선수": 4, "코너킥": 3, "프리킥": 3}},
]```
"""

# ERROR MESSAGES
INPUT_VERIFIER_ERR: str = "입력값을 해석할 수 없습니다. 제 쪽에서 문제가 생긴 것 같습니다. 관리자에게 문의해주세요"
ROUTER_ERR: str = "라우터 쪽에서 문제가 생긴 것 같습니다. 관리자에게 문의해주세요"
INDIV_TACTIC_ERR: str = (
    "개인 전술 업데이트 쪽에서 문제가 생긴 것 같습니다. 관리자에게 문의해주세요"
)
TEAM_TACTIC_ERR: str = (
    "팀 전술 업데이트 쪽에서 문제가 생긴 것 같습니다. 관리자에게 문의해주세요"
)

INVALID_QUERY_ERR: str = """제가 답할 수 없는 질문입니다. 축구 전술 관련된 질문을 해주시면 기꺼이 대답해드리겠습니다. 
ex) 2010년도 바르셀로나 전술을 구현하고 싶어
"""

CHATBOT_ERR: str = "전술 챗봇에서 문제가 생긴 것 같습니다. 관리자에게 문의해주세요"

QUERY_EXAMPLES: list[str] = [
    "안녕 자기 소개를 부탁해!",
    "공격시 윙 백이 빠른 속도로 상대편 수비진을 돌파하여 크로스를 보낼 수 있는 전술을 개발해줘.",
    "2010년도 펩 과르디올라 감독의 바르셀로나 전술을 구현하고 싶어",
    "수비라인을 높게 유지하면서 공격을 시작하는 전술을 마련해줘.",
    "공격할 때 중앙 공격수와 윙어 간의 연계를 강화하는 전술을 고안해줘.",
    "윙백을 과감하게 오버래핑시켜!",
    "게겐 프레싱하자!",
    "폴스 나인을 시도하면서 양쪽 윙어들의 라인 브레이킹을 시도해",
]
