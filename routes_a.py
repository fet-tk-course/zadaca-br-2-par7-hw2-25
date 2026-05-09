from fastapi import APIRouter, Depends, HTTPException, Query
from sqlmodel import Session, select
from typing import Optional

from database import get_session
from models_a import Restaurant, RestaurantCreate, RestaurantUpdate

router = APIRouter(prefix="/restaurants", tags=["Restaurants"])


@router.get("/")
def get_all_restaurants(
    is_open: Optional[bool] = Query(default=None, description="Filtriraj po tome da li restoran radi"),
    session: Session = Depends(get_session)
):
    query = select(Restaurant)
    # Primjena filtera ako je poslan u zahtjevu
    if is_open is not None:
        query = query.where(Restaurant.is_open == is_open)
    
    restaurants = session.exec(query).all()
    return restaurants

@router.get("/{restaurant_id}")
def get_restaurant(restaurant_id: int, session: Session = Depends(get_session)):
    restaurant = session.get(Restaurant, restaurant_id)
    # Vraća 404 grešku ako resurs nije pronađen
    if not restaurant:
        raise HTTPException(status_code=404, detail=f"Restoran sa ID-om {restaurant_id} nije pronađen")
    return restaurant


@router.post("/", status_code=201)  
def create_restaurant(restaurant: RestaurantCreate, session: Session = Depends(get_session)):
    new_restaurant = Restaurant.from_orm(restaurant)
    session.add(new_restaurant)
    session.commit()
    session.refresh(new_restaurant)
    return new_restaurant


@router.put("/{restaurant_id}")
def update_restaurant(restaurant_id: int, restaurant_update: RestaurantCreate, session: Session = Depends(get_session)):
    restaurant = session.get(Restaurant, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail=f"Restoran sa ID-om {restaurant_id} nije pronađen")
    
    restaurant_data = restaurant_update.dict()
    for key, value in restaurant_data.items():
        setattr(restaurant, key, value)
    
    session.add(restaurant)
    session.commit()
    session.refresh(restaurant)
    return restaurant


@router.patch("/{restaurant_id}")
def partial_update_restaurant(restaurant_id: int, restaurant_update: RestaurantUpdate, session: Session = Depends(get_session)):
    restaurant = session.get(Restaurant, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail=f"Restoran sa ID-om {restaurant_id} nije pronađen")
    
   
    restaurant_data = restaurant_update.dict(exclude_unset=True) 
    for key, value in restaurant_data.items():
        setattr(restaurant, key, value)
    
    session.add(restaurant)
    session.commit()
    session.refresh(restaurant)
    return restaurant


@router.delete("/{restaurant_id}", status_code=204)  # Status 204 za uspješno brisanje
def delete_restaurant(restaurant_id: int, session: Session = Depends(get_session)):
    restaurant = session.get(Restaurant, restaurant_id)
    if not restaurant:
        raise HTTPException(status_code=404, detail=f"Restoran sa ID-om {restaurant_id} nije pronađen")
    
    session.delete(restaurant)
    session.commit()
    return None