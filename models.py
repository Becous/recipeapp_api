from sqlalchemy import Column, Integer, String, Float, CheckConstraint, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class Item(Base):
    __tablename__ = "item"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    price = Column(Float)

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    surname = Column(String)
    password = Column(String)
    recipe = Column()

    saved_recipe = relationship("SaveRecipe", back_populates="user", cascade="all, delete")
    comment = relationship("Comment", back_populates="user", cascade="all, delete")


class Recipe(Base):
    __tablename__ = "recipe"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    rating = Column(Integer, CheckConstraint('rating >= 1 AND rating <= 5'))
    desc = Column(String)
    time_cook = Column(Integer)
    
    saved_by_user = relationship("SavedRecipe", back_populates="recipe", cascade="all, delete")


class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    text = Column(String)
    user_id = Column(Integer, ForeignKey("user.id"), nullable=True)
    recipe_id = Column(Integer, ForeignKey("recipe.id"))

    user = relationship("User", back_populates="comments")
    recipe = relationship("Recipe", back_populates="comments")

class SavedRecipe(Base):
    __tablename__ = "saved_recipe"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("user.id"))
    recipe_id = Column(Integer, ForeignKey("recipe.id"))

    user = relationship("User", back_populates="comments")
    recipe = relationship("Recipe", back_populates="comments")

    

    