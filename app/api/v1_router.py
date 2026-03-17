from fastapi import APIRouter, HTTPException
from app.schemas.user_dto import UserCreate, UserResponse
from app.schemas.product_dto import ProductCreate, ProductResponse
from app.schemas.meal_dto import MealLogCreate, MealLogResponse
from app.services.nutrition_service import nutrition_service

router = APIRouter()

@router.post("/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    return nutrition_service.create_user(user)

@router.post("/products", response_model=ProductResponse, status_code=201)
async def create_product(product: ProductCreate):
    return nutrition_service.create_product(product)

@router.get("/products", response_model=list[ProductResponse])
async def get_products():
    return nutrition_service.products

@router.post("/meals", response_model=MealLogResponse, status_code=201)
async def log_meal(meal: MealLogCreate):
    try:
        return nutrition_service.log_meal(meal)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e))