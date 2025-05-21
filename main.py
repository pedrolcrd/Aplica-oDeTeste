import os
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List
from pymongo import MongoClient
from dotenv import load_dotenv

# Carrega variáveis de ambiente
load_dotenv()

env_uri = os.getenv("MONGO_URI")
env_db = os.getenv("MONGO_DB")
if not env_uri or not env_db:
    raise RuntimeError("Variáveis MONGO_URI e MONGO_DB devem estar definidas em .env")

# Conexão MongoDB síncrona
client = MongoClient(env_uri)
db = client[env_db]

app = FastAPI()

# Modelos
class Item(BaseModel):
    id: str
    name: str

class ItemCreate(BaseModel):
    name: str

# Endpoints síncronos
@app.get("/items", response_model=List[Item])
def get_items():
    docs = list(db.items.find({}, {"name": 1}))
    return [Item(id=str(doc["_id"]), name=doc["name"]) for doc in docs]

@app.post("/items", response_model=Item, status_code=201)
def create_item(item: ItemCreate):
    res = db.items.insert_one(item.dict())
    return Item(id=str(res.inserted_id), name=item.name)
