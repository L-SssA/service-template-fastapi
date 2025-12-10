import uvicorn

from app.config import config
from app.server import app

uvicorn.run(
    app,
    host=config.listen_host,
    port=config.listen_port,
    log_level=config.log_level,
    reload=config.reload_debug,
)
