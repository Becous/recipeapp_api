from pydantic import BaseModel, conint
from typing import Union

class Item(BaseModel):
    name: str
    price: float
    is_offer: Union[bool, None] = None


class Recipe(BaseModel):
    name: str
    rating: conint(ge=1, le=5) # type: ignore
    desc: str
    time_cook: int
