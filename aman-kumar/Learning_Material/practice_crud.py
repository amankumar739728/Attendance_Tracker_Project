from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional

app = FastAPI()

class Item(BaseModel):
    id: Optional[int] = 1
    name: str = "aman"
    description: Optional[str] = "Sample item description"
    price: float =23

item_list=[]

@app.get("/")
def read_root():
    return {"message": "Welcome to the CRUD API"}

@app.post("/create_item/", response_model=Item)
def create_item(item: Item):
    item_dict = item.dict()
    item_list.append(item_dict)
    return item

@app.get("/items/", response_model=List[Item])
def read_items():
    return item_list

@app.get("/items/{item_id}", response_model=Item)
def read_item(item_id: int):
    for i in item_list:
        if i['id'] == item_id:
            return i
    raise HTTPException(status_code=404, detail="Item not found")

#query parameter(search the item by name)
@app.get("/items/search/")
def search_items(name: Optional[str] = None):
    if name is None:
        raise HTTPException(status_code=400, detail="Name query parameter is required")
    results = [i for i in item_list if name.lower() in i['name'].lower()]
    if not results:
        raise HTTPException(status_code=404, detail="No items found with the given name")
    return results

@app.put("/items/{item_id}", response_model=Item)
def update_item(item_id: int, item: Item):
    for i in item_list:
        if i['id'] == item_id:
            i.update(item.dict())
            return i
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/{item_id}", response_model=Item)
def delete_item(item_id: int):
    for i in item_list:
        if i['id'] == item_id:
            item_list.remove(i)
            return i
    raise HTTPException(status_code=404, detail="Item not found")

@app.delete("/items/")
def delete_all_items():
    if not item_list or len(item_list) == 0:
        raise HTTPException(status_code=404, detail="No items to delete")
    item_list.clear()
    return {"message": "All items deleted successfully"}


