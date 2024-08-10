from typing import Union
from fastapi import FastAPI
from database import engine, Sessionlocal, Base

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


@app.get("/items/{item_id}")
def read_item(item_id: int, q: Union[str, None] = None):
    return {"item_id": item_id, "q": q}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: models.Item):
    return {"item_name": item.name, "item_id": item_id}