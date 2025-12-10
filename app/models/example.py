from pydantic import Field
from .base import BaseResponse, IBaseModel


class ExampleRequest(IBaseModel):
    id: int = Field(..., description="id")
    name: str = Field(..., description="name")

class ExampleResponse(BaseResponse):
    class Config:
        json_schema_extra = {
            "example": {
                "code": 200,
                "data": {},
                "message": "操作成功",
            },
        }
