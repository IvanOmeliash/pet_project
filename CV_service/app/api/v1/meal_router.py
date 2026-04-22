from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from app.schemas.meal_dto import MealLogCreate, MealLogResponse
from app.core.database import get_db
from app.models.entities import ProductModel, MealLogModel
from app.services.user_client import get_remote_user

router = APIRouter()


@router.post("/", response_model=MealLogResponse, status_code=201)
async def log_meal(meal: MealLogCreate, db: Session = Depends(get_db)):
    user = await get_remote_user(meal.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found in User Service")

    product = db.query(ProductModel).filter(ProductModel.id == meal.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    calc_calories = (product.calories_100g / 100) * meal.weight_grams
    db_meal = MealLogModel(**meal.model_dump(), calories_burned=round(calc_calories, 2))
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal


@router.get("/", response_model=List[MealLogResponse])
def read_meals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(MealLogModel).offset(skip).limit(limit).all()


@router.put("/{meal_id}", response_model=MealLogResponse)
async def update_meal_log(meal_id: int, meal_update: MealLogCreate, db: Session = Depends(get_db)):
    user = await get_remote_user(meal_update.user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found in User Service")

    db_meal = db.query(MealLogModel).filter(MealLogModel.id == meal_id).first()
    if not db_meal:
        raise HTTPException(status_code=404, detail="Meal log not found")

    product = db.query(ProductModel).filter(ProductModel.id == meal_update.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    new_calories = (product.calories_100g / 100) * meal_update.weight_grams
    for key, value in meal_update.model_dump().items():
        setattr(db_meal, key, value)

    setattr(db_meal, "calories_burned", round(new_calories, 2))
    db.commit()
    db.refresh(db_meal)
    return db_meal


@router.delete("/{meal_id}", status_code=204)
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    db_meal = db.query(MealLogModel).filter(MealLogModel.id == meal_id).first()
    if not db_meal:
        raise HTTPException(status_code=404, detail="Meal log not found")
    db.delete(db_meal)
    db.commit()
    return None