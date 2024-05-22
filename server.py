from fastapi import FastAPI
import uvicorn
from middleware.auth import AuthMiddleware
from cmd_arg import arg
from cofreq import api_router

app = FastAPI()

app.add_middleware(AuthMiddleware)

app.include_router(api_router)


def start_server():
    uvicorn.run(app, host=arg.host, port=arg.port, log_level=arg.log_level)
