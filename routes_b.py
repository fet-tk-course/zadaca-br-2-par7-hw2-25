from typing import Optional

from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlmodel import Session, select

from database import get_session
from models_b import Food, FoodCreate, FoodUpdate

router = APIRouter(prefix="/foods", tags=["Foods"])

@router.get("/")
def get_foods(restaurant_id: Optional[int] = Query(default=None), session: Session = Depends(get_session)):
    query = select(Food)

    if restaurant_id is not None:
        query = query.where(Food.restaurant_id == restaurant_id)

    foods = session.exec(query).all()

    if restaurant_id is not None and not foods:
        raise HTTPException(status_code=404, detail="Nema dostupnih jela")

    return foods

@router.get("/{food_id}")
def get_food(food_id: int, session: Session = Depends(get_session)):
    food = session.get(Food, food_id)
    if not food:
        raise HTTPException(status_code=404, detail=f"Jelo sa ID-om {food_id} nije pronađeno")
    return food


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
        raise HTTPException(status_code=404, detail=f"Jelo sa ID-om {food_id} nije pronađeno")
    
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
        raise HTTPException(status_code=404, detail=f"Jelo sa ID-om {food_id} nije pronađeno")
    
    food_data = food_update.dict(exclude_unset=True)
    for key, value in food_data.items():
        setattr(food, key, value)
    
    session.add(food)
    session.commit()
    session.refresh(food)
    return food

@router.delete("/{food_id}", status_code=204)
def delete_food(food_id: int, session: Session = Depends(get_session)):
    food = session.get(Food, food_id)
    if not food:
        raise HTTPException(status_code=404, detail=f"Jelo sa ID-om {food_id} nije pronađeno")
    
    session.delete(food)
    session.commit()
    return None