from fastapi import APIRouter
from cofreq.api.cohere import cohere_router
from cofreq.api.groq_api import groq_router
from cofreq.api.chatglm import chatglm_router

api_router = APIRouter(
    prefix="/api",
)
api_router.include_router(cohere_router)
api_router.include_router(groq_router)
api_router.include_router(chatglm_router)
