from fastapi import FastAPI

app = FastAPI()

iteams = []

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/items")
def create_item(item: str):
    iteams.append(item)
    return iteams 
