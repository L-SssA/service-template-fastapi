from loguru import logger

from app.utils import http_utils
from app.utils.decorators import exception_handler
from app.routers.base import create_router
from app.models.example import (
    ExampleRequest,
    ExampleResponse,
)

router = create_router("example")


@router.post("/", summary="示例接口", response_model=ExampleResponse)
@exception_handler("处理任务")
async def example(body: ExampleRequest):
    logger.info(body)
    if body.id == 1:
        raise Exception("测试异常")
    return http_utils.get_response(code=200, message="操作成功")
