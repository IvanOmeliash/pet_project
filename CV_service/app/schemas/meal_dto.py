from pydantic import BaseModel, Field
from datetime import datetime

class MealLogCreate(BaseModel):
    user_id: int
    product_id: int
    weight_grams: float = Field(..., gt=0)

class MealLogResponse(MealLogCreate):
    id: int
    consumed_at: datetime
    calories_burned: float