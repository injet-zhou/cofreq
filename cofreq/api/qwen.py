from openai import OpenAI

import time
from typing import Annotated
from fastapi import APIRouter, Header
from sse_starlette import EventSourceResponse
from cofreq.models.chat import (
    ChatCompletions,
)
from cofreq.models.model import ModelsResponse, Datum

qwen_router = APIRouter(
    prefix="/qwen",
)

supported_models = [
    "qwen-turbo",
    "qwen-plus",
    "qwen-max",
    "qwen-max-0428",
    "qwen-max-0403",
    "qwen-max-0107",
    "qwen-max-longcontext",
    "qwen1.5-110b-chat",
    "qwen1.5-72b-chat",
    "qwen1.5-32b-chat",
    "qwen1.5-14b-chat",
    "qwen1.5-7b-chat",
    "qwen1.5-1.8b-chat",
    "qwen1.5-0.5b-chat",
    "codeqwen1.5-7b-chat",
    "qwen-72b-chat",
    "qwen-14b-chat",
    "qwen-7b-chat",
    "qwen-1.8b-longcontext-chat",
    "qwen-1.8b-chat",
]

qwen_unspported_fields = [
    "logprobs",
    "logit_bias",
    "top_logprobs",
    "functions",
    "function_call",
    "response_format",
    "user",
]


@qwen_router.get("/models")
async def get_models():
    return ModelsResponse(
        object="list",
        data=[
            Datum(
                id=model,
                object="model",
                created=int(time.time()),
                owned_by="openai",
            )
            for model in supported_models
        ],
    )


@qwen_router.post("/chat/completions")
async def chat_completions(
    chat: ChatCompletions,
    authorization: Annotated[str | None, Header()],
):
    api_key = authorization.removeprefix("Bearer ")
    client = OpenAI(
        api_key=api_key,
        base_url="https://dashscope.aliyuncs.com/compatible-mode/v1",
    )
    chat_params = chat.model_dump(exclude_none=True)
    # remove unsupported fields
    for field in qwen_unspported_fields:
        chat_params.pop(field, None)

    if not chat.stream:
        return client.chat.completions.create(**chat_params)

    rsp = client.chat.completions.create(**chat_params)

    def chat_stream():
        for response in rsp:
            yield response.model_dump_json()

    return EventSourceResponse(chat_stream())
