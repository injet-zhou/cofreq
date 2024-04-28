from fastapi import APIRouter
from cofreq.api.cohere import cohere_router

api_router = APIRouter(
    prefix="/api",
)
api_router.include_router(cohere_router)