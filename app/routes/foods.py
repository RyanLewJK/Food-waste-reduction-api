from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import SessionLocal
from app import models, schemas

router = APIRouter(prefix="/foods", tags=["Foods"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/", response_model=schemas.FoodItemResponse)
def create_food(food: schemas.FoodItemCreate, db: Session = Depends(get_db)):
    db_food = models.FoodItem(**food.dict())
    db.add(db_food)
    db.commit()
    db.refresh(db_food)
    return db_food

@router.get("/", response_model=list[schemas.FoodItemResponse])
def get_foods(db: Session = Depends(get_db)):
    return db.query(models.FoodItem).all()

@router.get("/{food_id}", response_model=schemas.FoodItemResponse)
def get_food(food_id: int, db: Session = Depends(get_db)):
    food = db.query(models.FoodItem).filter(models.FoodItem.id == food_id).first()
    return food

@router.put("/{food_id}", response_model=schemas.FoodItemResponse)
def update_food(food_id: int, food: schemas.FoodItemCreate, db: Session = Depends(get_db)):
    db_food = db.query(models.FoodItem).filter(models.FoodItem.id == food_id).first()

    if db_food:
        db_food.name = food.name
        db_food.category = food.category
        db_food.purchase_date = food.purchase_date
        db_food.expiry_date = food.expiry_date
        db_food.quantity = food.quantity
        db_food.location = food.location

        db.commit()
        db.refresh(db_food)

    return db_food

@router.delete("/{food_id}")
def delete_food(food_id: int, db: Session = Depends(get_db)):
    db_food = db.query(models.FoodItem).filter(models.FoodItem.id == food_id).first()

    if db_food:
        db.delete(db_food)
        db.commit()

    return {"message": "Food item deleted"}

from datetime import date, timedelta

@router.get("/expiring-soon/")
def get_expiring_food(days: int = 3, db: Session = Depends(get_db)):
    target_date = date.today() + timedelta(days=days)

    foods = db.query(models.FoodItem).filter(
        models.FoodItem.expiry_date <= target_date
    ).all()

    return foods