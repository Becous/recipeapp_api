from sqlalchemy import Column, Integer, String, Float, CheckConstraint, Boolean
from database import Base

# class Item(BaseModel):
#     name: str
#     price: float
#     is_offer: Union[bool, None] = None


# class Recipe(BaseModel):
#     name: str
#     rating: conint(ge=1, le=5) # type: ignore
#     desc: str
#     time_cook: int


class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)



class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    rating = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'))
    desc = Column(String)
    time_cook = Column(Integer)