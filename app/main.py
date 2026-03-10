from fastapi import FastAPI
from app.database import Base, engine
from app import models
from app.routes import foods

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Food Waste Reduction API")

app.include_router(foods.router)

@app.get("/")
def root():
    return {"message": "Food Waste Reduction API is running"}