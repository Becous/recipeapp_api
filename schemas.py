from pydantic import BaseModel, Field
from typing import List, Optional

# schemas.py

class CommentBase(BaseModel):
    text: str
    user_id: Optional[int]
    recipe_id: int

class CommentCreate(CommentBase):
    pass

class CommentInRecipe(CommentBase):
    id: int
    user_id: Optional[int]  # Не включаємо повний об'єкт User
    recipe_id: int

    class Config:
        orm_mode = True

class UserBase(BaseModel):
    name: str
    surname: str

class UserCreate(UserBase):
    password: str

class UserInComment(UserBase):
    id: int

    class Config:
        orm_mode = True

class RecipeBase(BaseModel):
    name: str
    rating: int = Field(..., ge=1, le=5)
    desc: str
    time_cook: int

class RecipeCreate(RecipeBase):
    pass

class RecipeInComment(RecipeBase):
    id: int

    class Config:
        orm_mode = True

# Повні схеми для серіалізації
class Comment(CommentBase):
    id: int
    user: Optional[UserInComment]
    recipe: Optional[RecipeInComment]

    class Config:
        orm_mode = True

class User(UserBase):
    id: int
    saved_recipes: List['SavedRecipe'] = []
    comments: List[CommentInRecipe] = []  # Використовуємо скорочену схему

    class Config:
        orm_mode = True

class Recipe(RecipeBase):
    id: int
    saved_by_users: List['SavedRecipe'] = []
    comments: List[CommentInRecipe] = []  # Використовуємо скорочену схему

    class Config:
        orm_mode = True

# SavedRecipe схеми
class SavedRecipeBase(BaseModel):
    user_id: int
    recipe_id: int

class SavedRecipeCreate(SavedRecipeBase):
    pass

class SavedRecipe(SavedRecipeBase):
    id: int
    user: UserInComment  # Використовуємо скорочену схему
    recipe: RecipeInComment  # Використовуємо скорочену схему

    class Config:
        orm_mode = True
