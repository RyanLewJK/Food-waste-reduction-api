from datetime import date
from pydantic import BaseModel

class FoodItemCreate(BaseModel):
    name: str
    category: str
    purchase_date: date
    expiry_date: date
    quantity: int
    location: str

class FoodItemResponse(FoodItemCreate):
    id: int
    status: str

    class Config:
        from_attributes = True