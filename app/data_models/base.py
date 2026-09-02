from typing import Any, Optional
from pydantic import BaseModel


class IBaseModel(BaseModel):
    __max_length__ = 200

    def __trim_string__(self, input_var):
        max_length = self.__max_length__
        # 判断是否为字符串
        if isinstance(input_var, str):
            # 判断字符串长度是否大于 max_length
            if len(input_var) > max_length:
                # 裁剪字符串并添加trim标记
                return input_var[:max_length] + "..."
            else:
                # 字符串长度小于或等于 max_length，不裁剪
                return input_var
        # 非字符串，直接返回原变量
        return input_var

    def __repr_args__(self):
        for k, v in self.__dict__.items():
            field = self.model_fields.get(k)
            if field and field.repr:
                yield k, self.__trim_string__(v)

        try:
            pydantic_extra = object.__getattribute__(
                self, '__pydantic_extra__')
        except AttributeError:
            pydantic_extra = None

        if pydantic_extra is not None:
            yield from ((k, self.__trim_string__(v)) for k, v in pydantic_extra.items())
        yield from ((k, self.__trim_string__(getattr(self, k))) for k, v in self.__class__.model_computed_fields.items() if v.repr)


class BaseResponse(IBaseModel):
    code: int = 200
    data: Any = None
    message: Optional[str] = '操作成功'
