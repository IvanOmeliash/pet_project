from sqlalchemy import Column, Integer, String, Float, ForeignKey, DateTime
from sqlalchemy.sql import func
from app.core.database import Base

class ProductModel(Base):
    __tablename__ = "products"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True, index=True)
    calories_100g = Column(Float)
    protein = Column(Float)
    fat = Column(Float)
    carbs = Column(Float)

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    weight = Column(Float)
    height = Column(Float)
    target_calories = Column(Integer)

class MealLogModel(Base):
    __tablename__ = "meal_logs"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    product_id = Column(Integer, ForeignKey("products.id"))
    weight_grams = Column(Float)
    calories_burned = Column(Float)
    consumed_at = Column(DateTime, server_default=func.now())