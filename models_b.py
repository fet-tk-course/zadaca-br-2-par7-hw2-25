from sqlmodel import SQLModel, Field
from typing import Optional

class Food(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    restaurant_id: int = Field(foreign_key="restaurant.id")
    name: str
    category: str
    price: float
    calories: int
    available: bool = True
    description: Optional[str] = None

class FoodCreate(SQLModel):
    name: str
    restaurant_id: int
    category: str
    price: float
    calories: int
    available: bool = True
    description: Optional[str] = None

class FoodUpdate(SQLModel):
    name: Optional[str] = None
    restaurant_id: Optional[int] = None
    category: Optional[str] = None
    price: Optional[float] = None
    calories: Optional[int] = None
    available: Optional[bool] = None
    description: Optional[str] = None