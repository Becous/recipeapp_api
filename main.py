from fastapi import FastAPI, Depends, HTTPException
from database import engine, Sessionlocal, Base
from sqlalchemy.orm import Session
from models import Item, Recipe

import models

app = FastAPI()

Base.metadata.create_all(bind=engine)

def get_db():
    db = Sessionlocal()
    try: 
        yield db
    except: 
        db.close()

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/items")
def create_item(name: str, price:float, db: Session = Depends(get_db)):
    item = Item(name = name, price = price)
    db.add(item)
    db.commit()
    db.refresh(item)
    return item

@app.get("/items/{item_id}")
def show_item(item_id:int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item is None:
        raise HTTPException(status_code=404, detail="Items not Found")
    return item

@app.get("/items")
def show_item(db: Session = Depends(get_db)):
    item = db.query(Item).all()
    if item is None:
        raise HTTPException(status_code=404, detail="Items not Found")
    return item

@app.delete("/items/")
def delete_item(item_id:int, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    db.delete(item)
    db.commit()

    return item

@app.put("/items/{item_id}/update")
def update_item(item_id: int,name: str, price: float, db: Session = Depends(get_db)):
    item = db.query(Item).filter(Item.id == item_id).first()
    if item:
        item.name = name
        item.price = price
        db.commit()
        db.refresh(item)
    else: 
        raise HTTPException(status_code=404, detail="Items not Found")
    
    return item