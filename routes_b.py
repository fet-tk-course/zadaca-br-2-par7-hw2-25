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
