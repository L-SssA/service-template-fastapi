
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

def register_cors_middleware(app: FastAPI):
    # cors 设置
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["*"],
        allow_methods=["*"],
        allow_headers=["*"],
        allow_credentials=True,
    )

def register_middleware(app: FastAPI):
    register_cors_middleware(app)
