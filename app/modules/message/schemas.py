from typing import List

from app.shared.schemas import IBaseModel, BaseResponse
from pydantic import Field


class EmailModel(IBaseModel):
    addresses: List[str] = Field(..., description="Email 地址列表")
