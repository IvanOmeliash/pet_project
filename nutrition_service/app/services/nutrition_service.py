from datetime import datetime
from app.schemas.product_dto import ProductCreate, ProductResponse
from app.schemas.meal_dto import MealLogCreate, MealLogResponse


class NutritionService:
    def __init__(self):
        self.users = []
        self.products = []
        self.meals = []
        self._u_counter = 1
        self._p_counter = 1
        self._m_counter = 1

    # Logic for Products
    def create_product(self, data: ProductCreate) -> ProductResponse:
        product = ProductResponse(id=self._p_counter, **data.model_dump())
        self.products.append(product)
        self._p_counter += 1
        return product

    # Business Logic: Logging a meal with calculation
    def log_meal(self, data: MealLogCreate) -> MealLogResponse:
        product = next((p for p in self.products if p.id == data.product_id), None)
        if not product:
            raise ValueError("Product not found")
        # Розрахунок калорій на основі ваг

        calc_calories = (product.calories_100g / 100) * data.weight_grams

        meal = MealLogResponse(
            id=self._m_counter,
            consumed_at=datetime.now(),
            calories_burned=round(calc_calories, 2),
            **data.model_dump()
        )
        self.meals.append(meal)
        self._m_counter += 1
        return meal


# Singleton instance
nutrition_service = NutritionService()