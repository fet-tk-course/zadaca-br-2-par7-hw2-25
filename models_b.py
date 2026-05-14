from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator

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

    @field_validator("name")
    @classmethod 
    def naziv_ne_smije_biti_prazan(cls, value):
        if not value.strip():
            raise ValueError('Name ne smije biti prazan string')
        
    @classmethod
    def naziv_mora_imatt_min_duzinu(cls, value):
        if len(value.strip()) < 2:
            raise ValueError('Name mora imati minimalnu dužinu od 2 znaka')
        return value.strip()
  
    @field_validator('price')
    @classmethod
    def price_mora_biti_pozitivan(cls,v):
        if v <= 0:
            raise ValueError('Price mora biti veća od nule')
        return v

   