import uvicorn

from app.config import config

if __name__ == "__main__":
    uvicorn.run(
        "app.server:app",
        host=config.listen_host,
        port=config.listen_port,
        log_level=config.log_level,
        reload=config.reload_debug,
        reload_dirs=["app"],
    )
