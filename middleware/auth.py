from fastapi.responses import JSONResponse
from starlette.types import ASGIApp
from starlette.middleware.base import BaseHTTPMiddleware


class AuthMiddleware(BaseHTTPMiddleware):
    def __init__(self, app: ASGIApp) -> None:
        self.app = app

    async def dispatch_func(self, request, call_next):
        authorization = request.headers.get("Authorization")
        path = request.url.path
        if path.endswith("/chat/completions"):
            if not authorization:
                return JSONResponse(
                    status_code=401, content={"detail": "Authorization header required"}
                )
            if not authorization.startswith("Bearer "):
                return JSONResponse(
                    status_code=401, content={"detail": "Bearer token required"}
                )
            if not authorization.strip("Bearer "):
                return JSONResponse(
                    status_code=401, content={"detail": "Bearer token required"}
                )
        response = await call_next(request)
        return response
