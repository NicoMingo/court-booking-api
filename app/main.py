from fastapi import FastAPI
from .routers import courts, auth, bookings
from .database import engine
from . import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(auth.router)
app.include_router(courts.router)
app.include_router(bookings.router)

@app.get("/")
def welcome_page():
    return {"message": "This is the welcome page"}