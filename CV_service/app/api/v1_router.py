from fastapi import APIRouter
from app.api.v1.product_router import router as product_router
from app.api.v1.meal_router import router as meal_router

router = APIRouter()

router.include_router(product_router, prefix="/products", tags=["Products"])
router.include_router(meal_router, prefix="/meals", tags=["Meals"])