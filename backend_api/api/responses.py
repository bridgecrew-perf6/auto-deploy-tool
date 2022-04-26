from typing import Generic, Optional, TypeVar

from pydantic.generics import GenericModel

# class Usuario(BaseModel):
#     id: int
#     nome:str
#     email:str


DataType = TypeVar('DataType')


class IResponseBaseJson(GenericModel, Generic[DataType]):

    status: int
    message: str
    data: Optional[DataType] = None
