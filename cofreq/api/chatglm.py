from typing import Annotated
import time

from fastapi import APIRouter, Header
from sse_starlette import EventSourceResponse
from cofreq.models.chat import (
    ChatCompletions,
    # ChatCompletionResponse,
    # ChatCompletionChunkResponse,
    # ChatCompletionChunkChoice,
    # ChatCompletionChunkDelta,
    # Choice,
    # Message,
    # Usage,
)
from cofreq.models.model import ModelsResponse, Datum
from zhipuai import ZhipuAI
from zhipuai.types.chat.chat_completion import Completion

supported_models = ["glm-4", "glm-3-turbo"]

chatglm_router = APIRouter(
    prefix="/chatglm",
)

chatgml_unspported_fields = [
    "logprobs",
    "logit_bias",
    "top_logprobs",
    "functions",
    "function_call",
    "frequency_penalty",
    "response_format",
    "n",
    "presence_penalty",
    "user",
]


def new_chatglm(api_key):
    client = ZhipuAI(api_key=api_key)
    return client


@chatglm_router.get("/models")
async def get_models():
    return ModelsResponse(
        object="list",
        data=[
            Datum(
                id=model,
                object="model",
                created=int(time.time()),
                owned_by="zhipuai",
            )
            for model in supported_models
        ],
    )


def to_chat_params(chat: ChatCompletions):
    params = chat.model_dump()
    for field in chatgml_unspported_fields:
        params.pop(field, None)
    return params


def chatglm_chat(chat: ChatCompletions, authorization: str):
    chat_params = to_chat_params(chat)
    print("authorization:", authorization)
    client = new_chatglm(api_key=authorization.removeprefix("Bearer "))
    response: Completion = client.chat.completions.create(**chat_params)
    return response


def chatglm_stream_chat(chat: ChatCompletions, authorization: str):
    chat_params = to_chat_params(chat)
    client = new_chatglm(api_key=authorization.removeprefix("Bearer "))
    response = client.chat.completions.create(**chat_params)
    return response


@chatglm_router.post("/chat/completions")
async def chat_completions(
    chat: ChatCompletions,
    authorization: Annotated[str | None, Header()],
):
    if not chat.stream:
        return chatglm_chat(chat, authorization)
    rsp = chatglm_stream_chat(chat, authorization)

    def chat_stream():
        for response in rsp:
            yield response.model_dump_json()

    return EventSourceResponse(chat_stream())
