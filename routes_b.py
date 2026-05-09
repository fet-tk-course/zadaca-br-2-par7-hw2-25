from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select

from database import get_session
from models_b import Food, FoodCreate, FoodUpdate

router = APIRouter(prefix="/foods", tags=["Foods"])