from sqlmodel import SQLModel, Field
from typing import Optional

class Restaurant(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: str
    cuisine_type: str
    delivery_fee: float
    rating: int
    is_open: bool = True
    address: Optional[str] = None

class RestaurantCreate(SQLModel):
    name: str
    cuisine_type: str
    delivery_fee: float
    rating: int
    is_open: bool = True
    address: Optional[str] = None


class RestaurantUpdate(SQLModel):
    name: Optional[str] = None
    cuisine_type: Optional[str] = None
    delivery_fee: Optional[float] = None
    rating: Optional[int] = None
    is_open: Optional[bool] = None
    address: Optional[str] = None