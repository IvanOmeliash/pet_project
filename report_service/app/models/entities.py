from sqlalchemy import Column, Integer, String, Float
from app.core.database import Base

class UserModel(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    weight = Column(Float)
    height = Column(Float)
    target_calories = Column(Integer)

