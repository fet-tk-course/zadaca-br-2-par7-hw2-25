from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from database import get_session
from models_b import Food, FoodCreate, FoodUpdate

router = APIRouter(prefix="/foods", tags=["Foods"])

@router.get("/")
def get_all_foods(session: Session = Depends(get_session)):
    foods = session.exec(select(Food)).all()
    return foods

@router.get("/{food_id}")
def get_food(food_id: int, session: Session = Depends(get_session)):
    food = session.get(Food, food_id)
    if not food:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Food not found")
    return food

@router.get("/restaurants/{restaurant_id}")
def get_foods_by_restaurant(restaurant_id: int, session: Session = Depends(get_session)):
    foods = session.exec(select(Food).where(Food.restaurant_id == restaurant_id)).all()
    return foods

@router.post("/", status_code=201)
def create_food(food: FoodCreate, session: Session = Depends(get_session)):
    new_food = Food.from_orm(food)
    session.add(new_food)
    session.commit()
    session.refresh(new_food)
    return new_food

@router.put("/{food_id}")
def update_food(food_id: int, food_update: FoodCreate, session: Session = Depends(get_session)):
    food = session.get(Food, food_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    food_data = food_update.dict(exclude_unset=True)
    for key, value in food_data.items():
        setattr(food, key, value)
    
    session.add(food)
    session.commit()
    session.refresh(food)
    return food

@router.patch("/{food_id}")
def partial_update_food(food_id: int, food_update: FoodUpdate, session: Session = Depends(get_session)):
    food = session.get(Food, food_id)
    if not food:
        raise HTTPException(status_code=404, detail="Food not found")
    
    food_data = food_update.dict(exclude_unset=True)
    for key, value in food_data.items():
        setattr(food, key, value)
    
    session.add(food)
    session.commit()
    session.refresh(food)
    return food