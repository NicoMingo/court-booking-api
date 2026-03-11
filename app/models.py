from sqlalchemy import Column, String, Integer, Boolean, DATE, TIME, FLOAT, DateTime, TIMESTAMP, text
from .database import Base # Muy importante

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key = True, nullable = False)
    email = Column(String, unique = True, nullable = False)
    password = Column(String, nullable = False)
    full_name = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))

class Court(Base):
    __tablename__ = 'courts'
    
    id = Column(Integer, primary_key = True, nullable = False)
    name = Column(String, nullable = False)
    sport_type = Column(String, nullable = False)
    price_per_hour = Column(FLOAT, nullable = False)
    is_available = Column(Boolean, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))

class Booking(Base):
    __tablename__ = 'bookings'

    id = Column(Integer, primary_key = True, nullable = False)
    user_id = Column(Integer, nullable = False)
    court_id = Column(Integer, nullable = False)
    booking_date = Column(DATE, nullable = False)
    start_time = Column(TIME, nullable = False)
    end_time = Column(TIME, nullable = False)
    total_price = Column(FLOAT, nullable= False)
    status = Column(String, nullable = False)
    created_at = Column(TIMESTAMP(timezone = True), nullable = False, server_default = text('now()'))


#3 Tablas INDEPENDIENTES (sin foreign keys):
# 1. Users

# id
# email (único)
# password (hasheado)
# full_name
# created_at

# 2. Courts (Canchas)

# id
# name (ej: "Cancha Fútbol 5 - A")
# sport_type (ej: "football", "tennis")
# price_per_hour
# is_available (boolean)
# created_at

# 3. Bookings (Reservas)

# id
# user_email (texto simple)
# court_id (número simple)
# booking_date
# start_time
# end_time
# total_price
# status ("pending", "confirmed", "cancelled")
# created_at