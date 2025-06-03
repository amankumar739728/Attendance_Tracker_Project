#install packages using : pip install fastapi uvicorn

from fastapi import FastAPI

app = FastAPI()

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

@app.get("/items/{item_id}")
def read_item(item_id: int, q: str = None):
    return {"item_id": item_id, "query": q}

#query parameters:
@app.get("/items/")
def read_items(skip: int = 0, limit: int = 10):
    items = [{"item_id": i} for i in range(skip, skip + limit)]
    return {"items": items}


# To run the app, use the below command in the terminal from the directory where this file is located:
# uvicorn simple_fastapi:app --reload