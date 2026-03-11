from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, database, oauth2
from ..database import get_db
from datetime import datetime

router = APIRouter(
    prefix = "/bookings",
    tags = ["Bookings"]
)


@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.BookingOut)
def create_booking(booking: schemas.BookingCreate, current_user_id: schemas.TokenData = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    check_time_available = db.query(models.Booking).filter(models.Booking.court_id == booking.court_id,
                                                                models.Booking.booking_date == booking.booking_date,
                                                                models.Booking.start_time < booking.end_time,
                                                                models.Booking.end_time > booking.start_time).first()
    
    if check_time_available is None:
        get_price_per_hour = db.query(models.Court.price_per_hour).filter(models.Court.id == booking.court_id).scalar()

        booking_start_time = datetime.combine(booking.booking_date, booking.start_time)
        booking_end_time = datetime.combine(booking.booking_date, booking.end_time)
        total_booking_time = (booking_end_time - booking_start_time).total_seconds() / 3600

        created_booking = models.Booking(user_id = current_user_id.id,
                                        court_id = booking.court_id,
                                        booking_date = booking.booking_date,
                                        start_time = booking.start_time,
                                        end_time = booking.end_time,
                                        total_price = total_booking_time * get_price_per_hour,
                                        status = "booked")
        
        db.add(created_booking)
        db.commit()
        db.refresh(created_booking)
        
        return created_booking
    else:
        # return "not available" -> no se puede poner esto, se debe hacer un raise exception debido a que ya le prometimos al response model que ibamos a devolver un schemas.BookingOut
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="La cancha ya está reservada en ese horario")

@router.get("/", status_code = status.HTTP_200_OK, response_model = List[schemas.BookingOutList])
def get_all_bookings(db: Session = Depends(get_db)):
    booking_list = db.query(models.Booking).all()

    return booking_list

@router.get("/{id}", status_code = status.HTTP_200_OK, response_model = schemas.BookingOutList)
def get_specific_booking(id: int, db: Session = Depends(get_db)):
    get_booking = db.query(models.Booking).filter(models.Booking.id == id).first()

    if get_booking is None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "The booking requested was not found")
    
    return get_booking