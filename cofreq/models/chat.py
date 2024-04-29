from __future__ import annotations

import time
from typing import Any, List, Optional

from pydantic import BaseModel, Field


class Message(BaseModel):
    role: str
    content: str
    # tool_call_id: Optional[str] = None


class Function(BaseModel):
    name: str
    description: str


class Tool(BaseModel):
    type: str
    function: Function


class FunctionCall(BaseModel):
    name: str


class ResponseFormat(BaseModel):
    type: str


class Function2(BaseModel):
    name: str


class ToolChoice(BaseModel):
    type: str
    function: Function2


class ChatCompletions(BaseModel):
    model: str
    messages: List[Message]
    logprobs: Optional[bool] = False
    tools: Optional[List[Tool]] = None
    functions: Optional[List[Function]] = None
    top_logprobs: Optional[int] = None
    frequency_penalty: Optional[float] = None
    logit_bias: Optional[dict] = None
    function_call: Optional[FunctionCall] = None
    response_format: Optional[ResponseFormat] = None
    n: Optional[int] = 1
    stream: Optional[bool] = False
    presence_penalty: Optional[float] = None
    user: Optional[str] = None
    seed: Optional[int] = None
    # tool_choice: Optional[ToolChoice] = None
    top_p: Optional[float] = None
    max_tokens: Optional[int] = None
    temperature: Optional[float] = None
    stop: Optional[str] = None


class Choice(BaseModel):
    index: int
    message: Message
    logprobs: Any
    finish_reason: str


class Usage(BaseModel):
    prompt_tokens: int
    completion_tokens: int
    total_tokens: int


class ChatCompletionResponse(BaseModel):
    id: str
    object: str
    created: Optional[int] = Field(default_factory=lambda: int(time.time()))
    model: str
    # system_fingerprint: Optional[str]
    choices: List[Choice]
    usage: Optional[Usage] = None


class ChatCompletionChunkResponse(BaseModel):
    id: str
    object: str
    created: Optional[int] = Field(default_factory=lambda: int(time.time()))
    model: str
    # system_fingerprint: Optional[str]
    choices: List[ChatCompletionChunkChoice]


class ChatCompletionChunkDelta(BaseModel):
    role: Optional[str]
    content: Optional[str]


class ChatCompletionChunkChoice(BaseModel):
    index: int
    delta: ChatCompletionChunkDelta
    finish_reason: Optional[str]
    logprobs: Optional[Any]
