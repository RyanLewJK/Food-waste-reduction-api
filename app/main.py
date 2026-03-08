from fastapi import FastAPI

app = FastAPI(title="Food Waste Reduction API")

@app.get("/")
def root():
    return {"message": "Food Waste Reduction API is running"}
