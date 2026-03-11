from fastapi import APIRouter, HTTPException, status, Depends
from sqlalchemy.orm import Session
from ..database import get_db
from .. import schemas, database, utils, models, oauth2

router = APIRouter(
    prefix = "/auth",
    tags = ["Auth"]
)

@router.post("/signup", response_model = schemas.UserOut, status_code = status.HTTP_201_CREATED)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    new_user = models.User(email = user.email, password = hashed_password, full_name = user.full_name)
    
    db.add(new_user)
    db.commit()
    
    return new_user

@router.post("/login")
def login(user: schemas.UserLogin, db: Session = Depends(get_db)):
    username_info = db.query(models.User).filter(models.User.email == user.email).first()

    if username_info is None:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    
    verify_user = utils.verify(user.password, username_info.password)

    if verify_user is False:
        raise HTTPException(status_code = status.HTTP_401_UNAUTHORIZED)
    
    access_token = oauth2.create_access_token({"user_id": username_info.id})

    return {"access_token": access_token, "token_type": "bearer"}

# OJO CON EL current_user_id
@router.get("/users/me", response_model = schemas.UserOut)
def show_user_information(current_user_id: schemas.TokenData = Depends(oauth2.get_current_user), db: Session = Depends(get_db)):

    user_info = db.query(models.User).filter(models.User.id == current_user_id.id).first()

    return user_info