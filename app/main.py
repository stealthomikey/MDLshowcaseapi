
from fastapi import FastAPI
from app.routers import meals  

# Create an instance of the FastAPI application
app = FastAPI(
    title="MDL Showcase API",
    description="used for the backend logic for the caloire counting app.",
    version="1.0.0",
)

app.include_router(meals.router)

# confirm the API is running
@app.get("/", tags=["Root"])
def read_root():
    return {"Hello world"}