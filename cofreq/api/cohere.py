import cohere
from typing import Annotated
from fastapi import APIRouter, Header, HTTPException
from sse_starlette import EventSourceResponse
from cofreq.models.chat import (
    ChatCompletions,
    ChatCompletionResponse,
    ChatCompletionChunkResponse,
    ChatCompletionChunkChoice,
    ChatCompletionChunkDelta,
    Choice,
    Message,
    Usage,
)
from cohere.types.chat_message import ChatMessage
from cohere.types.non_streamed_chat_response import NonStreamedChatResponse
from cohere.types.streamed_chat_response import (
    StreamedChatResponse_StreamStart,
    StreamedChatResponse_TextGeneration,
    StreamedChatResponse_StreamEnd,
)

cohere_router = APIRouter(
    prefix="/cohere",
)


def new_cohere(api_key):
    co = cohere.Client(api_key)
    return co


cohere_role_map = {
    "user": "USER",
    "assistant": "CHATBOT",
    "system": "SYSTEM",
}


@cohere_router.get("/models")
async def get_models():
    return ["command-r-plus"]


def to_chat_params(chat: ChatCompletions):
    messages = chat.messages

    message = messages.pop().content
    chat_history = [
        ChatMessage(role=cohere_role_map[msg.role], message=msg.content)
        for msg in messages
    ]
    chat_params = {
        "message": message,
        "chat_history": chat_history,
        "model": chat.model,
        "temperature": chat.temperature,
        "p": chat.top_p,
        "frequency_penalty": chat.frequency_penalty,
        "presence_penalty": chat.presence_penalty,
        "seed": chat.seed,
        "max_tokens": chat.max_tokens,
    }
    return chat_params


def cohere_chat(chat: ChatCompletions, authorization: str):
    chat_params = to_chat_params(chat)
    co = new_cohere(authorization.strip("Bearer "))
    if not chat.stream:
        rsp: NonStreamedChatResponse = co.chat(**chat_params)
        response = ChatCompletionResponse(
            id=rsp.generation_id,
            object="chat.completion",
            model=chat.model,
            choices=[
                Choice(
                    index=0,
                    message=Message(role="assistant", content=rsp.text),
                    logprobs=None,
                    finish_reason="stop",
                )
            ],
            usage=Usage(
                prompt_tokens=rsp.meta.tokens.input_tokens,
                completion_tokens=rsp.meta.tokens.output_tokens,
                total_tokens=rsp.meta.tokens.input_tokens
                + rsp.meta.tokens.output_tokens,
            ),
        )
    return response


def cohere_stream_chat(chat: ChatCompletions, authorization: str):
    chat_params = to_chat_params(chat)
    co = new_cohere(authorization.strip("Bearer "))
    stream_rsp = co.chat_stream(**chat_params)
    for chunk in stream_rsp:
        if isinstance(chunk, StreamedChatResponse_StreamStart):
            continue
        if isinstance(chunk, StreamedChatResponse_TextGeneration):
            yield ChatCompletionChunkResponse(
                id="",
                object="chat.completion.chunk",
                model=chat.model,
                choices=[
                    ChatCompletionChunkChoice(
                        index=0,
                        delta=ChatCompletionChunkDelta(
                            role="assistant", content=chunk.text
                        ),
                        logprobs=None,
                        finish_reason="incomplete",
                    ),
                ],
            ).model_dump_json()
        if isinstance(chunk, StreamedChatResponse_StreamEnd):
            yield ChatCompletionChunkResponse(
                id=chunk.response.generation_id,
                object="chat.completion.chunk",
                model=chat.model,
                choices=[
                    ChatCompletionChunkChoice(
                        index=0,
                        delta=ChatCompletionChunkDelta(role="assistant", content=""),
                        logprobs=None,
                        finish_reason="stop",
                    ),
                ],
            ).model_dump_json()


@cohere_router.post("/chat/completions")
async def chat_completions(
    chat: ChatCompletions, authorization: Annotated[str | None, Header()]
):
    messages = chat.messages
    if messages[-1].role != "user":
        raise HTTPException(
            status_code=400, detail="The last message must be from the user"
        )
    if not chat.stream:
        rsp = cohere_chat(chat, authorization)
        return rsp

    return EventSourceResponse(cohere_stream_chat(chat, authorization))
