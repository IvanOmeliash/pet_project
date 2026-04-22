from pydantic import BaseModel, Field

class ProductBase(BaseModel):
    name: str = Field(..., min_length=2)
    calories_100g: float = Field(..., gt=0)
    protein: float = Field(default=0, ge=0)
    fat: float = Field(default=0, ge=0)
    carbs: float = Field(default=0, ge=0)

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int

    class Config:
        from_attributes = True