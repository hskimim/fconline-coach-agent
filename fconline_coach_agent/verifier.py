from ast import literal_eval

from fconline_coach_agent import constant, models, utils
from fconline_coach_agent.data import indiv_tactic
from fconline_coach_agent.prompts import router
from fconline_coach_agent.prompts import verifier as verifier_prompt


def verify_input(query: str, current_tactic: str, tol: int = 5) -> bool:
    msg = verifier_prompt.input_verifier_prompt.format(question=query)
    cnt = 0
    result_ok = False
    while cnt < tol:
        results = models.ModelClient().run(
            question=msg, model=constant.MODEL_NM, temperature=0
        )[0]
        if results in ["True", "False"]:
            result_ok = True
            break
        cnt += 1
    if result_ok is False:
        return False
    else:
        if literal_eval(results) is False:
            return False

    result = team_tactic_output_verifier(current_tactic, mode="json")
    if result is False:
        return False
    return True


def team_tactic_json_verifier(data: str) -> bool:
    response = data.strip()
    head_condition = response.startswith("```json")
    end_condition = response.endswith("```")

    if head_condition and end_condition:
        try:
            json_data = utils.convert_markdownjson_to_json(response)
        except Exception:
            return False
    else:
        return False
    for mapped_tactic in json_data:
        if not isinstance(mapped_tactic, dict):
            return False
        comp_name = list(mapped_tactic.keys())[0]
        comp_val = mapped_tactic[comp_name]
        match comp_name:
            case "포메이션":
                if not isinstance(comp_val, str):
                    return False
                if "-" not in comp_val:
                    return False
                if comp_val.replace("-", "") not in constant.FORMATION_POSITION_MAPPER:
                    return False

            case "수비 스타일":
                if not isinstance(comp_val, str):
                    return False
                if comp_val not in [
                    "후퇴",
                    "밸런스",
                    "지속적인 압박",
                    "볼 터치 실수 시 압박",
                    "공 뺏긴 직후 압박",
                ]:
                    return False

            case "빌드업 플레이":
                if not isinstance(comp_val, str):
                    return False
                if comp_val not in ["느린 빌드업", "밸런스", "긴 패스", "빠른 빌드업"]:
                    return False

            case "수비 포지셔닝":
                if not isinstance(comp_val, dict):
                    return False
                if len(set(comp_val.keys()) - set(["폭", "깊이"])) != 0:
                    return False
                for _, v in comp_val.items():
                    if not (isinstance(v, int) and (v >= 1) and (v <= 10)):
                        return False

            case "공격 포지셔닝":
                if not isinstance(comp_val, dict):
                    return False
                if (
                    len(
                        set(comp_val.keys())
                        - set(["폭", "박스 안 쪽 선수", "코너킥", "프리킥"])
                    )
                    != 0
                ):
                    return False
                for _, v in comp_val.items():
                    if not (isinstance(v, int) and (v >= 1) and (v <= 10)):
                        return False
            case _:
                return False
    return True


def team_tactic_output_verifier(response: str, mode: str) -> bool:
    if mode == "json":
        return team_tactic_json_verifier(response)
    elif mode == "narrative":
        if constant.SEPERATOR not in response:
            return False
        return team_tactic_json_verifier(response.split(constant.SEPERATOR)[1])
    else:
        raise ValueError("Invalid Mode")


def router_verifier(response: str, multi: bool = False, friendly: bool = False) -> bool:
    head_condition = response.startswith("```json")
    end_condition = response.endswith("```")

    if head_condition and end_condition:
        try:
            json_data = utils.convert_markdownjson_to_json(response)
        except Exception:
            return False
    else:
        return False
    if multi:
        if not isinstance(json_data, list):
            return False
        for data in json_data:
            if not ("destination" in data and "next_inputs" in data):
                return False
            if not isinstance(data, dict):
                return False
            if data["destination"] not in router.model_mapper:
                return False
            if not friendly and data["destination"] == "DEFAULT":
                return False
    else:
        if not ("destination" in json_data and "next_inputs" in json_data):
            return False
        if not isinstance(json_data, dict):
            return False
        if json_data["destination"] not in router.model_mapper:
            return False
        if not friendly and json_data["destination"] == "DEFAULT":
            return False
    return True


def indiv_tactic_output_verifier(response: str, mode: str = "json") -> bool:
    if mode == "json":
        return indiv_tactic_json_verifier(response)
    elif mode == "narrative":
        if constant.SEPERATOR not in response:
            return False
        return indiv_tactic_json_verifier(response.split(constant.SEPERATOR)[1])
    else:
        raise ValueError("Invalid Mode")


def indiv_tactic_json_verifier(data: str) -> bool:
    response = data.strip()
    head_condition = response.startswith("```json")
    end_condition = response.endswith("```")

    if head_condition and end_condition:
        try:
            json_data = utils.convert_markdownjson_to_json(response)
        except Exception:
            return False
    else:
        return False
    if not isinstance(json_data, list):
        return False
    if not isinstance(json_data[0], dict):
        return False
    if len(set(len(data_dict) for data_dict in json_data)) != 1:
        return False
    if not all(
        [
            set(data_dict.keys()) == {"formation", "key", "value"}
            for data_dict in json_data
        ]
    ):
        return False
    for data_dict in json_data:
        if not isinstance(data_dict, dict):
            return False
        if data_dict["key"] not in indiv_tactic.indiv_tactic_dict:
            return False
        if data_dict["value"] not in indiv_tactic.indiv_tactic_dict[data_dict["key"]]:
            return False
    return True
