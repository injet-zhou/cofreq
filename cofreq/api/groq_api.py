import time
from typing import Annotated
from groq import Groq
from fastapi import APIRouter, Header
from sse_starlette import EventSourceResponse
from cofreq.models.chat import (
    ChatCompletions,
)
from cofreq.models.model import ModelsResponse, Datum

groq_router = APIRouter(
    prefix="/groq",
)

supported_models = [
    "llama3-8b-8192",
    "llama3-70b-8192",
    "mixtral-8x7b-32768",
    "gemma-7b-it",
]

groq_unspported_fields = [
    "logprobs",
    "logit_bias",
    "top_logprobs",
    "functions",
    "function_call",
]


@groq_router.get("/models")
async def get_models():
    return ModelsResponse(
        object="list",
        data=[
            Datum(
                id=model,
                object="model",
                created=int(time.time()),
                owned_by="groq",
            )
            for model in supported_models
        ],
    )


@groq_router.post("/chat/completions")
async def chat_completions(
    chat: ChatCompletions,
    authorization: Annotated[str | None, Header()],
):
    client = Groq(
        api_key=authorization.strip("Bearer "),
    )
    chat_params = chat.model_dump()
    # remove unsupported fields
    for field in groq_unspported_fields:
        chat_params.pop(field, None)

    chat_params["n"] = 1
    chat_completion = client.chat.completions.create(**chat_params)
    if not chat.stream:
        return chat_completion

    return EventSourceResponse(chat_completion)
