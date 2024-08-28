from fastapi import FastAPI, Depends, HTTPException
from database import engine, Sessionlocal, Base
from sqlalchemy.orm import Session, joinedload
import models
import schemas

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = Sessionlocal()
    try:
        yield db
    except Exception as e:
        print(f"Error in get_db: {str(e)}")  # Логування помилки
        raise
    finally:
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}


## ITEM TEST FUNC

# @app.post("/items")
# def create_item(name: str, price:float, db: Session = Depends(get_db)):
#     item = models.Item(name = name, price = price)
#     db.add(item)
#     db.commit()
#     db.refresh(item)
#     return item

# @app.get("/items/{item_id}")
# def show_item(item_id:int, db: Session = Depends(get_db)):
#     item = db.query(models.Item).filter(models.Item.id == item_id).first()
#     if item is None:
#         raise HTTPException(status_code=404, detail="Items not Found")
#     return item

# @app.get("/items")
# def show_item(db: Session = Depends(get_db)):
#     item = db.query(models.Item).all()
#     if item is None:
#         raise HTTPException(status_code=404, detail="Items not Found")
#     return item

# @app.delete("/items/")
# def delete_item(item_id:int, db: Session = Depends(get_db)):
#     item = db.query(models.Item).filter(models.Item.id == item_id).first()
#     db.delete(item)
#     db.commit()

#     return item

# @app.put("/items/{item_id}/update")
# def update_item(item_id: int,name: str, price: float, db: Session = Depends(get_db)):
#     item = db.query(models.Item).filter(models.Item.id == item_id).first()
#     if item:
#         item.name = name
#         item.price = price
#         db.commit()
#         db.refresh(item)
#     else: 
#         raise HTTPException(status_code=404, detail="Items not Found")
    
#     return item



## User FUNC
@app.post("/users/", response_model=schemas.User) #Сторення користувача
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User == user.name).first()
    if db_user:
        raise HTTPException(status_code=404, detail="User already exist")
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@app.get("/users/{user_id}", response_model=schemas.User)
def show_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not Found")
    return db_user

@app.get("/users/", response_model=list[schemas.User])
def show_all_user(db: Session = Depends(get_db)):
    db_users = db.query(models.User).all()
    return db_users


@app.put("/users/{user_id}/", response_model=schemas.User)
def update_user(user_id: int, name:str, surname: str, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db_user.name = name
        db_user.surname = surname
        db.commit()
        db.refresh(db_user)
    else:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user

@app.delete("/users/{user_id}/")
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    db.delete()
    db.commit()
    return db_user


## RECIPE FUNC

@app.post("/recipes/", response_model=schemas.Recipe)
def create_recipe(recipe: schemas.RecipeCreate, db: Session = Depends(get_db)):
    new_recipe = models.Recipe(
        name=recipe.name,
        rating=recipe.rating,
        desc=recipe.desc,
        time_cook=recipe.time_cook,
    )
    db.add(new_recipe)
    db.commit()
    db.refresh(new_recipe)
    return new_recipe


@app.get("/recipes/{recipe_id}/", response_model=schemas.Recipe)
def show_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not Found")
    return db_recipe

@app.get("/recipe/", response_model=list[schemas.Recipe])
def show_all_recipe(db: Session = Depends(get_db)):
    db_recipe = db.query(models.Recipe).all()
    if db_recipe is None:
        raise HTTPException(status_code=404, detail="Recipe not Found")
    return db_recipe


@app.delete("/recipes/{recipe_id}", response_model=schemas.Recipe)
def delete_recipe(recipe_id: int, db: Session = Depends(get_db)):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe_id).first()
    db.delete(db_recipe)
    db.commit()
    return db_recipe

@app.put("/recipes/{recipe_id}/", response_model=schemas.Recipe)
def update_recipe(recipe: schemas.Recipe, db: Session = Depends(get_db)):
    db_recipe = db.query(models.Recipe).filter(models.Recipe.id == recipe.id).first()
    if db_recipe: 
        db_recipe.name = recipe.name
        db_recipe.desc = recipe.desc
        db_recipe.rating = recipe.rating
        db_recipe.time_cook = recipe.time_cook
        db_recipe.saved_by_users = recipe.saved_by_users
        db.commit()
        db.refresh(db_recipe)
    else:
        raise HTTPException(status_code=404, detail="Recipe not Found")
    return db_recipe

## Comment section 
@app.post("/comments/", response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    new_comment = models.Comment(**comment.dict())
    db.add(new_comment)
    db.commit()
    db.refresh(new_comment)
    return new_comment

@app.get("/recipes/{recipe_id}/comments/", response_model=list[schemas.Comment])
def read_all_comments(recipe_id: int, db: Session = Depends(get_db)):
    comments = db.query(models.Comment).filter(models.Comment.recipe_id == recipe_id).all()
    return comments

@app.get("/comments/", response_model=list[schemas.Comment])
def read_all_comments(db: Session = Depends(get_db)):
    comments = db.query(models.Comment).all()
    return comments


@app.get("/comments/{com_id}/", response_model=schemas.Comment)
def read_comment(com_id: int, db: Session = Depends(get_db)):
    comment = db.query(models.Comment)\
                .options(joinedload(models.Comment.user), joinedload(models.Comment.recipe))\
                .filter(models.Comment.id == com_id)\
                .first()
    if comment is None:
        raise HTTPException(status_code=404, detail="Comment not found")
    return comment

@app.delete("/comments/{com_id}/", response_model=schemas.Comment)
def delete_comment(com_id: int, db: Session = Depends(get_db)):
    # Шукаємо коментар за його ID
    comment = db.query(models.Comment).filter(models.Comment.id == com_id).first()

    # Якщо коментар не знайдений, повертаємо помилку
    if not comment:
        raise HTTPException(status_code=404, detail="Comment not found")

    # Видаляємо коментар з бази даних
    db.delete(comment)
    db.commit()

    # Повертаємо видалений коментар як відповідь
    return {"msg": "Success"}