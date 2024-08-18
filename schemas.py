from pydantic import BaseModel, Field
from typing import List, Optional

class ItemBase(BaseModel):
    name: str
    price: float

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    name: str
    surname: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    saved_recipes: List['SavedRecipe'] = []
    comments: List['Comment'] = []

    class Config:
        orm_mode = True

class RecipeBase(BaseModel):
    name: str
    rating: int = Field(..., ge=1, le=5)
    desc: str
    time_cook: int

class RecipeCreate(RecipeBase):
    pass

class Recipe(RecipeBase):
    id: int
    saved_by_users: List['SavedRecipe'] = []
    comments: List['Comment'] = []

    class Config:
        orm_mode = True


class CommentBase(BaseModel):
    text: str
    user_id: Optional[int]
    recipe_id: int

class CommentCreate(CommentBase):
    pass

class Comment(CommentBase):
    id: int
    user: Optional[User]
    recipe: Optional[Recipe]

    class Config:
        orm_mode = True


class SavedRecipeBase(BaseModel):
    user_id: int
    recipe_id: int

class SavedRecipeCreate(SavedRecipeBase):
    pass

class SavedRecipe(SavedRecipeBase):
    id: int
    user: User
    recipe: Recipe

    class Config:
        orm_mode = True
