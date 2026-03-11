from pydantic import BaseModel, EmailStr
from datetime import date, datetime, time
from typing import Optional

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    full_name: str

class UserOut(BaseModel):
    email: EmailStr
    full_name: str
    created_at: datetime

    class Config():
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class CourtBooking(BaseModel):
    name: str
    sport_type: str
    price_per_hour: float
    is_available: bool

class CourtBookingOut(BaseModel):
    name: str
    sport_type: str
    price_per_hour: float
    is_available: bool

    class Config:
        from_attributes = True

class BookingOutList(BaseModel):
    court_id: int
    booking_date: date
    start_time: time
    end_time: time

    class Config:
        from_attributes = True

class BookingCreate(BaseModel):
    court_id: int
    booking_date: date
    start_time: time
    end_time: time

class BookingOut(BaseModel):
    booking_date: date
    start_time: time
    end_time: time
    total_price: float

    class Config:
        from_attributes = True

class TokenData(BaseModel):
    id: Optional[int] = None

