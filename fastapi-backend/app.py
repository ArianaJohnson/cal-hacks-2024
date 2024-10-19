from fastapi import FastAPI
from pydantic import BaseModel

app = FastAPI()

class Item(BaseModel):
    name: str
    description: str

# Simple endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Hackathon API"}

# POST endpoint for React Native app
@app.post("/items/")
def create_item(item: Item):
    return {"name": item.name, "description": item.description}
