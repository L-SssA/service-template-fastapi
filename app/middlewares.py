
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def register_cors_middleware(app: FastAPI):
    # cors 设置
    cors_allow_origins = ["*"]
    app.add_middleware(
        CORSMiddleware,
        allow_origins=cors_allow_origins,
        allow_credentials=True,
        allow_methods=["*"],
        allow_headers=["*"],
    )

def register_middleware(app: FastAPI):
    register_cors_middleware(app)
