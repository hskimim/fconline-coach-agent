import asyncio

from dotenv import load_dotenv
from openai import AsyncOpenAI, OpenAI

# import nest_asyncio
from openai.types.chat import ChatCompletionMessageParam  # type:ignore

from fconline_coach_agent import constant

load_dotenv()


class BaseAgent:
    def __init__(self, tol: int = 5) -> None:
        self._client = ModelClient()
        self._tol = tol


class ModelClient:
    def __init__(self) -> None:
        self._client = OpenAI()
        self._async_client = AsyncOpenAI()

    def run(self, question: str, **kwargs) -> list[str]:
        input_: list[ChatCompletionMessageParam] = [
            {"role": "user", "content": question}
        ]

        kwargs["model"] = kwargs.get("model", constant.MODEL_NM)
        kwargs["temperature"] = kwargs.get("temperature", constant.TEMPERATURE)

        response = self._client.chat.completions.create(
            messages=input_,
            **kwargs,
        )

        msg = response.choices[0].message.content
        if isinstance(msg, str):
            return [msg]
        else:
            raise ValueError

    async def _async_call(self, question: str, **kwargs) -> list[str]:
        input_: list[ChatCompletionMessageParam] = [
            {"role": "user", "content": question}
        ]

        kwargs["model"] = kwargs.get("model", constant.MODEL_NM)
        kwargs["temperature"] = kwargs.get("temperature", constant.TEMPERATURE)

        response = await self._async_client.chat.completions.create(
            messages=input_,
            **kwargs,
        )

        msg = response.choices[0].message.content
        if isinstance(msg, str):
            return [msg]
        else:
            raise ValueError

    async def _async_calls(self, questions: list[str], **kwargs) -> list[list[str]]:
        result = await asyncio.gather(
            *[self._async_call(question, **kwargs) for question in questions]
        )
        return result

    def async_run(self, questions: list[str], **kwargs) -> list[list[str]]:
        return asyncio.run(self._async_calls(questions, **kwargs))
