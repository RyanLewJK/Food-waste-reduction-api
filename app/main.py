from fastapi import FastAPI
from app.database import Base, engine

Base.metadata.create_all(bind=engine)

app = FastAPI(title="Food Waste Reduction API")

@app.get("/")
def root():
    return {"message": "Food Waste Reduction API is running"}
