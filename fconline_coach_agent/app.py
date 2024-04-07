import logging
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(os.path.dirname(__file__))))
import gradio as gr  # type:ignore
import pandas as pd  # type:ignore

from fconline_coach_agent import gradio_utils
from fconline_coach_agent.agent import AudioAgent, MultiAgent


def predict(message, json_data):
    msg = AudioAgent().run(message).strip()
    logging.debug(msg)
    return MultiAgent(
        query=msg,
        current_tactic=json_data,
    ).update()


def process_input(
    text,
    audio,
    whitespace,
    formation,
    defensive_style,
    buildup_play,
    width_defense,
    depth_defense,
    width_attack,
    players_in_box,
    corner,
    free_kick,
) -> str:
    question, current_tactic = gradio_utils.preprocess_input(
        text,
        audio,
        whitespace,
        formation,
        defensive_style,
        buildup_play,
        width_defense,
        depth_defense,
        width_attack,
        players_in_box,
        corner,
        free_kick,
    )
    resps = predict(question, current_tactic)

    stacked_html = ""
    for resp in resps:
        match resp.mode:
            case "team_tactic":
                answer, dict_data = gradio_utils.postprocess_input(resp.answer)
                html_output = gradio_utils.get_team_tactic_html(answer, dict_data)
            case "indiv_tactic":
                answer, dict_data = gradio_utils.postprocess_input(resp.answer)
                if isinstance(dict_data, list):
                    component = dict_data
                elif isinstance(dict_data, dict):
                    component = [dict_data]
                else:
                    raise TypeError("invalid response type")

                html_output = pd.DataFrame(component).to_html()
                html_output = gradio_utils.html_header.format(text=answer) + html_output
            case "default":
                html_output = gradio_utils.get_casual_html(resp.answer)
            case _:
                raise ValueError(f"Unknown mode: {resp.mode}")
        stacked_html += html_output
    return stacked_html


# Gradio 인터페이스를 생성합니다.
interface = gr.Interface(
    fn=process_input,
    inputs=gradio_utils.get_input_interface(),
    outputs=gr.HTML(label="출력 결과"),  # "text",
    title="FC Agent",
    description="감독님의 현재 적용 중이신 팀 전술을 입력해주시고 원하시는 팀 전술을 자유롭게 써주시거나 말씀해주세요.",
)

# 인터페이스를 실행합니다.
interface.launch(debug=True)
