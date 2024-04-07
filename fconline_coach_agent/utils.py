from ast import literal_eval

import numpy as np
import tiktoken
from transformers import pipeline  # type:ignore


def convert_markdownjson_to_json(markdown: str) -> list[dict] | dict:
    markdown = markdown.replace("```json", "").replace("```", "")
    return literal_eval(markdown)


def convert_json_to_dict(json_: list[dict]) -> dict:
    result = {}
    for dict_ in json_:
        for k, v in dict_.items():
            if isinstance(v, dict):
                for i, j in v.items():
                    result[k + "_" + i] = j
            else:
                result[k] = v
    return result


def is_nested_json(data: list[dict]) -> bool:
    for dict_data in data:
        for _, v in dict_data.items():
            if isinstance(v, dict) or isinstance(v, set):
                return True
    return False


def convert_json2vec(json_, get_cols=False):
    scores = []
    columns = []

    for category, score_dict in json_[0].items():
        for sub_cat, score in score_dict.items():
            scores.append(score)
            columns.append(f"{category}-{sub_cat}")
    if get_cols:
        return scores, columns
    return scores


def get_token_length(sentence: str, model_nm: str = "gpt-4-turbo") -> int:
    return len(tiktoken.encoding_for_model(model_name=model_nm).encode(sentence))


def audio_predict(audio):
    sr, y = audio
    y = y.astype(np.float32)
    y /= np.max(np.abs(y))

    parsed = pipeline("automatic-speech-recognition", model="openai/whisper-tiny")(
        {"sampling_rate": sr, "raw": y}
    )["text"]
    return parsed
