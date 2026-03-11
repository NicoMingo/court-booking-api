from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from typing import List
from ..database import get_db
from .. import models, schemas, oauth2

router = APIRouter(
    prefix = "/courts",
    tags = ["Courts"]
)

@router.get("/", status_code = status.HTTP_200_OK, response_model = List[schemas.CourtBookingOut])
def list_all_courts(db: Session = Depends(get_db)):
    
    all_courts = db.query(models.Court).all()
    return all_courts

@router.get("/{id}", status_code=status.HTTP_200_OK, response_model=schemas.CourtBookingOut)
def get_specific_court(id: int, db: Session = Depends(get_db)):
    court = db.query(models.Court).filter(models.Court.id == id).first()
    if court is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="The requested court was not found")
    return court

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.CourtBookingOut)
def create_court( court: schemas.CourtBooking, current_user_id: schemas.TokenData = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):
    
    new_court = models.Court(**court.model_dump()) ## OJO: ESTO NO ME ACORDABA
    db.add(new_court)
    db.commit()
    db.refresh(new_court)

    return new_court