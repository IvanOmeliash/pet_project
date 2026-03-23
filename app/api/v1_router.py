from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional

from app.schemas.user_dto import UserCreate, UserResponse
from app.schemas.product_dto import ProductCreate, ProductResponse
from app.schemas.meal_dto import MealLogCreate, MealLogResponse
from app.core.database import get_db
from app.models.entities import ProductModel, UserModel, MealLogModel  # Додай MealLogModel

router = APIRouter()

@router.post("/products", response_model=ProductResponse, status_code=201, tags=["Products"])
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.get("/products", response_model=List[ProductResponse], tags=["Products"])
def read_products(skip: int = 0, limit: int = 10, search: Optional[str] = None, db: Session = Depends(get_db)):
    query = db.query(ProductModel)
    if search:
        query = query.filter(ProductModel.name.contains(search))
    return query.offset(skip).limit(limit).all()


@router.put("/products/{product_id}", response_model=ProductResponse, tags=["Products"])
def update_product(product_id: int, product_update: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product_update.model_dump().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product


@router.delete("/products/{product_id}", status_code=204, tags=["Products"])
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()
    return None


# --- USERS (Твоя логіка + Tags) ---

@router.post("/users", response_model=UserResponse, status_code=201, tags=["Users"])
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    db_user = UserModel(**user.model_dump())
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.get("/users", response_model=List[UserResponse], tags=["Users"])
def read_users(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(UserModel).offset(skip).limit(limit).all()


@router.put("/users/{user_id}", response_model=UserResponse, tags=["Users"])
def update_user(user_id: int, user_update: UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    for key, value in user_update.model_dump().items():
        setattr(db_user, key, value)
    db.commit()
    db.refresh(db_user)
    return db_user


@router.delete("/users/{user_id}", status_code=204, tags=["Users"])
def delete_user(user_id: int, db: Session = Depends(get_db)):
    db_user = db.query(UserModel).filter(UserModel.id == user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    db.delete(db_user)
    db.commit()
    return None


# --- MEALS (Новий блок для Лаби №2) ---

@router.post("/meals", response_model=MealLogResponse, status_code=201, tags=["Meals"])
def log_meal(meal: MealLogCreate, db: Session = Depends(get_db)):
    # Перевірка чи існують юзер та продукт
    product = db.query(ProductModel).filter(ProductModel.id == meal.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    # Розрахунок калорій (бізнес-логіка)
    calc_calories = (product.calories_100g / 100) * meal.weight_grams

    db_meal = MealLogModel(
        **meal.model_dump(),
        calories_burned=round(calc_calories, 2)
    )
    db.add(db_meal)
    db.commit()
    db.refresh(db_meal)
    return db_meal


@router.get("/meals", response_model=List[MealLogResponse], tags=["Meals"])
def read_meals(skip: int = 0, limit: int = 10, db: Session = Depends(get_db)):
    return db.query(MealLogModel).offset(skip).limit(limit).all()


@router.delete("/meals/{meal_id}", status_code=204, tags=["Meals"])
def delete_meal(meal_id: int, db: Session = Depends(get_db)):
    db_meal = db.query(MealLogModel).filter(MealLogModel.id == meal_id).first()
    if not db_meal:
        raise HTTPException(status_code=404, detail="Meal log not found")
    db.delete(db_meal)
    db.commit()
    return None


@router.put("/meals/{meal_id}", response_model=MealLogResponse, tags=["Meals"])
def update_meal_log(meal_id: int, meal_update: MealLogCreate, db: Session = Depends(get_db)):
    db_meal = db.query(MealLogModel).filter(MealLogModel.id == meal_id).first()
    if not db_meal:
        raise HTTPException(status_code=404, detail="Meal log not found")

    product = db.query(ProductModel).filter(ProductModel.id == meal_update.product_id).first()
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")

    new_calories = (product.calories_100g / 100) * meal_update.weight_grams

    update_data = meal_update.model_dump()
    for key, value in update_data.items():
        setattr(db_meal, key, value)

    db_model_extra = {"calories_burned": round(new_calories, 2)}
    setattr(db_meal, "calories_burned", db_model_extra["calories_burned"])

    db.commit()  # Транзакційність: фіксуємо зміни в Postgres
    db.refresh(db_meal)
    return db_meal