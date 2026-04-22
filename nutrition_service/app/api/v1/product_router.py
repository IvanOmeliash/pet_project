import json
from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from app.schemas.product_dto import ProductCreate, ProductResponse
from app.core.database import get_db
from app.models.entities import ProductModel
from app.core.redis_config import redis_client  # Імпортуємо наш клієнт

router = APIRouter()

CACHE_KEY_PRODUCTS = "products_list"
CACHE_EXPIRE = 60  # Кеш живе 60 секунд


@router.post("/", response_model=ProductResponse, status_code=201)
def create_product(product: ProductCreate, db: Session = Depends(get_db)):
    db_product = ProductModel(**product.model_dump())
    db.add(db_product)
    db.commit()
    db.refresh(db_product)

    # ПУНКТ 5: Інвалідація кешу (очищуємо, бо дані в базі змінилися)
    redis_client.delete(CACHE_KEY_PRODUCTS)

    return db_product


@router.get("/", response_model=List[ProductResponse])
def read_products(skip: int = 0, limit: int = 10, search: Optional[str] = None, db: Session = Depends(get_db)):
    # ПУНКТ 4: Перевірка кешу
    # Створюємо унікальний ключ для різних фільтрів
    cache_key = f"{CACHE_KEY_PRODUCTS}:{skip}:{limit}:{search}"
    cached_data = redis_client.get(cache_key)

    if cached_data:
        print("--- Віддаємо дані з REDIS ---")  # Для логів у звіті
        return json.loads(cached_data)

    print("--- Йдемо в базу даних (POSTGRES) ---")
    query = db.query(ProductModel)
    if search:
        query = query.filter(ProductModel.name.contains(search))

    products = query.offset(skip).limit(limit).all()

    # Перетворюємо об'єкти SQLAlchemy у словники для JSON
    products_json = [ProductResponse.model_validate(p).model_dump() for p in products]

    # Зберігаємо в Redis
    redis_client.setex(cache_key, CACHE_EXPIRE, json.dumps(products_json))

    return products


@router.delete("/{product_id}", status_code=204)
def delete_product(product_id: int, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    db.delete(db_product)
    db.commit()

    # ПУНКТ 5: Очищення кешу після видалення
    redis_client.delete(CACHE_KEY_PRODUCTS)

    return None

@router.put("/{product_id}", response_model=ProductResponse)
def update_product(product_id: int, product_update: ProductCreate, db: Session = Depends(get_db)):
    db_product = db.query(ProductModel).filter(ProductModel.id == product_id).first()
    if not db_product:
        raise HTTPException(status_code=404, detail="Product not found")
    for key, value in product_update.model_dump().items():
        setattr(db_product, key, value)
    db.commit()
    db.refresh(db_product)
    return db_product
