from typing import Union

from fastapi import FastAPI,Path,Query,Form,File,UploadFile  # type: ignore
from fastapi.staticfiles import StaticFiles # type: ignore
from pydantic import BaseModel  # type: ignore
from enum import Enum
app = FastAPI()
app.mount("/static",StaticFiles(directory="static"), name="static")

class Item(BaseModel):
    name:str
    price:float
    is_offer: Union[bool, None] = None
    
class ChoiceType(int,Enum):
   one=1
   two=2
   three=3

@app.get("/")
def read_root():
    return {"Hello": "World"}


@app.get("/items/{item_id}")
def read_item(item_id: int, q: str | None = None):
    item_get={"Hello":item_id}
    return {"item_id": item_get, "q": q}

@app.get("/query")
def query_fun(name: str, role_number: Union[int, None] =( Query(default=None, min_value=3, max_value=3))): 
    response = {
        "message": f"Hello, {name}!",
        "role_number": role_number if role_number is not None else "No role number provided"
    }
    return response

@app.get("/models/{model_name}")
def get_model(model_name: ChoiceType):
    
    return {"enum": model_name}

@app.put("/items/{item_id}")
def update_item(item_id: int, item: Item):
    return {"item_name": item.name, "item_id": item_id,"price":item.price}

@app.post("/form/data")
def form_data(user_name:str = Form,password:str = Form()):
    return {"user_name": user_name, "password":password}

@app.post("/file")
def file_bytes_len(file:bytes=File()):
    return ({"file": len(file)})

@app.post("/upload/file")
def file_upload(file: UploadFile):
    return ({"file": file})