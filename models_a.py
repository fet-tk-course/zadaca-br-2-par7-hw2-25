from sqlmodel import SQLModel, Field
from typing import Optional
from pydantic import field_validator


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


@field_validator('naziv')
@classmethod
def naziv_ne_smije_biti_prazan(cls, v):
    if not v.strip():
        raise ValueError('Naziv restorana ne smije biti prazan')
    return v.strip() 

@field_validator('ocjena')
@classmethod
def raspon_ocjene(cls, v):
    if v < 1 or v > 5:
        raise ValueError('Ocjena mora biti u rasponu od 1 do 5')
    return v




