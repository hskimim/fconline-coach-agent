import gradio as gr  # type:ignore

from fconline_coach_agent import utils


def generate_slider(label: str):
    return gr.Slider(minimum=1, maximum=10, step=1, label=label, value=3)


def generate_dropdown(label: str, choices: list[str], value: str = "밸런스"):
    return gr.Dropdown(choices=choices, label=label, value=value)


def generate_textbox(label: str):
    return gr.Textbox(label=label)


def generate_whitespace():
    return gr.components.HTML("<div style='margin-top: 20px;'></div>")


def generate_audio():
    return gr.Audio(sources=["microphone"])


def get_input_interface():
    return [
        generate_textbox(
            label="요청하시는 팀 전술 ex) 2010년도 바르셀로나 전술을 구현하고 줘, 윙백을 과감하게 오버래핑시켜!"
        ),
        generate_audio(),
        generate_whitespace(),
        generate_dropdown(
            label="포메이션",
            choices=[
                "4-4-2",
                "4-2-3-1",
                "4-3-3",
                "3-5-2",
                "3-4-3",
                "4-1-2-1-2",
                "4-3-2-1",
                "4-5-1",
                "5-3-2",
                "4-1-4-1",
                "4-1-3-2",
                "4-3-1-2",
            ],
            value="4-2-3-1",
        ),
        generate_dropdown(
            label="수비 스타일",
            choices=[
                "후퇴",
                "밸런스",
                "볼 터치 실수 시 압박",
                "공 뺏긴 직후 압박",
                "지속적인 압박",
            ],
        ),
        generate_slider(label="폭"),
        generate_slider(label="깊이"),
        generate_dropdown(
            label="빌드업 플레이",
            choices=["느린 빌드업", "밸런스", "긴 패스", "빠른 빌드업"],
        ),
        generate_slider(label="폭"),
        generate_slider(label="박스 안 쪽 선수"),
        generate_slider(label="코너킥"),
        generate_slider(label="프리킥"),
    ]


def preprocess_input(
    text,
    audio,
    _,
    formation,
    defensive_style,
    width_defense,
    depth_defense,
    buildup_play,
    width_attack,
    players_in_box,
    corner,
    free_kick,
) -> list[str]:
    data = [
        {"포메이션": formation},
        {"수비 스타일": defensive_style},
        {"빌드업 플레이": buildup_play},
        {"수비 포지셔닝": {"폭": width_defense, "깊이": depth_defense}},
        {
            "공격 포지셔닝": {
                "폭": width_attack,
                "박스 안 쪽 선수": players_in_box,
                "코너킥": corner,
                "프리킥": free_kick,
            }
        },
    ]
    if audio:
        text = utils.audio_predict(audio)
    current_tactic = "```json" + str(data) + "```"
    return [text, current_tactic]


def postprocess_input(response: str):
    text, tactic = response.split("```json")
    tactic = "```json" + tactic
    text = text.strip()
    tactic = tactic.strip()
    json_data = utils.convert_markdownjson_to_json(tactic)

    if isinstance(json_data, dict):
        return [text, json_data]

    if isinstance(json_data, list) and isinstance(json_data[0], dict):
        if utils.is_nested_json(json_data):
            return [text, utils.convert_json_to_dict(json_data)]
        else:
            return [text, json_data]
    raise TypeError("invalid type for response")


def get_team_tactic_html(
    text,
    dict_data,
) -> str:
    html_output = f"""
    <div style="font-family: sans-serif; color: #fff; background-color: #333; padding: 20px; border-radius: 10px; max-width: 500px; margin: 20px auto;">
    <h2 style="text-align: center; color: #4CAF50; margin-bottom: 20px;">전술 설정</h2>
    <div style="margin-bottom: 20px; text-align: center;">
        <label for="greeting" style="display: block; margin-bottom: 5px;">{text}</label>
    </div>
    <div style="margin-bottom: 10px;">
        <strong>포메이션:</strong> <span style="float: right;">{dict_data['포메이션']}</span>
    </div>
    <div style="margin-bottom: 10px;">
        <strong>수비 스타일:</strong> <span style="float: right;">{dict_data['수비 스타일']}</span>
    </div>
    <div style="margin-bottom: 10px;">
        <strong>빌드업 플레이:</strong> <span style="float: right;">{dict_data['빌드업 플레이']}</span>
    </div>
    <div style="margin-bottom: 20px;">
        <strong>수비 포지셔닝:</strong>
        <div style="margin-top: 5px;">
            <strong>폭:</strong>
            <div style="background-color: #ddd; border-radius: 10px; padding: 3px;">
                <div style="height: 20px; width: {int(dict_data['수비 포지셔닝_폭'] * 10)}%; background-color: #4CAF50; border-radius: 7px; text-align: center; line-height: 20px;">{dict_data['수비 포지셔닝_폭']}</div>
            </div>
        </div>
        <div style="margin-top: 5px;">
            <strong>깊이:</strong>
            <div style="background-color: #ddd; border-radius: 10px; padding: 3px;">
                <div style="height: 20px; width: {int(dict_data['수비 포지셔닝_깊이'] * 10)}%; background-color: #4CAF50; border-radius: 7px; text-align: center; line-height: 20px;">{dict_data['수비 포지셔닝_깊이']}</div>
            </div>
        </div>
    </div>
    <div style="margin-bottom: 20px;">
        <strong>공격 포지셔닝:</strong>
        <div style="margin-top: 5px;">
            <strong>폭:</strong>
            <div style="background-color: #ddd; border-radius: 10px; padding: 3px;">
                <div style="height: 20px; width: {int(dict_data['공격 포지셔닝_폭'] * 10)}%; background-color: #4CAF50; border-radius: 7px; text-align: center; line-height: 20px;">{dict_data['공격 포지셔닝_폭']}</div>
            </div>
        </div>
        <div style="margin-top: 5px;">
            <strong>박스 안 쪽 선수:</strong>
            <div style="background-color: #ddd; border-radius: 10px; padding: 3px;">
                <div style="height: 20px; width: {int(dict_data['공격 포지셔닝_박스 안 쪽 선수']*10)}%; background-color: #4CAF50; border-radius: 7px; text-align: center; line-height: 20px;">{dict_data['공격 포지셔닝_박스 안 쪽 선수']}</div>
            </div>
        </div>
        <div style="margin-top: 5px;">
            <strong>코너킥:</strong>
            <div style="background-color: #ddd; border-radius: 10px; padding: 3px;">
                <div style="height: 20px; width: {int(10 * dict_data['공격 포지셔닝_코너킥'])}%; background-color: #4CAF50; border-radius: 7px; text-align: center; line-height: 20px;">{dict_data['공격 포지셔닝_코너킥']}</div>
            </div>
        </div>
        <div style="margin-top: 5px;">
            <strong>프리킥:</strong>
            <div style="background-color: #ddd; border-radius: 10px; padding: 3px;">
                <div style="height: 20px; width: {int(10 * dict_data['공격 포지셔닝_프리킥'])}%; background-color: #4CAF50; border-radius: 7px; text-align: center; line-height: 20px;">{dict_data['공격 포지셔닝_프리킥']}</div>
            </div>
        </div>
    </div>
</div>

    """
    return html_output  # predict(text, current_tactic)


def get_casual_html(text):
    html_output = f"""
    <div style="font-family: sans-serif; color: #fff; background-color: #333; padding: 20px; border-radius: 10px; max-width: 500px; margin: 20px auto;">
    <h2 style="text-align: center; color: #4CAF50; margin-bottom: 20px;">전술 설정</h2>
    <div style="margin-bottom: 20px; text-align: center;">
        <label for="greeting" style="display: block; margin-bottom: 5px;">{text}</label>
    </div>    
</div>

    """
    return html_output


html_header = """<div style="font-family: sans-serif; color: #fff; background-color: #333; padding: 20px; border-radius: 10px; max-width: 500px; margin: 20px auto;">
    <h2 style="text-align: center; color: #4CAF50; margin-bottom: 20px;">전술 설정</h2>
    <div style="margin-bottom: 20px; text-align: center;">
        <label for="greeting" style="display: block; margin-bottom: 5px;">{text}</label>
    </div>"""
