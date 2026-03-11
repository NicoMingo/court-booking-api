from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from . import schemas
from fastapi.security import OAuth2PasswordBearer
import os
from dotenv import load_dotenv

load_dotenv() # Carga el archivo .env

oauth2_scheme = OAuth2PasswordBearer(tokenUrl = 'auth/login')

SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):
    # Recordar que data es toda la informacion del usuario que encriptariamos en la parte del medio (payload) del JWT como por ejemplo {"user_id": 5}
    # # ¿Por qué usamos data.copy()?
    # En Python, si le pasás un diccionario a una función y lo modificás adentro
    # (ej: agregándole la fecha de expiración "exp"), estás modificando el 
    # diccionario ORIGINAL que está afuera de la función en la memoria RAM.
    # Al usar .copy(), le sacamos una "fotocopia" exacta. Así podemos agregarle
    # la expiración a la copia para generar el token, dejando el diccionario
    # original intacto y limpio.
    to_encode = data.copy() 

    expire = datetime.now(timezone.utc) + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm = ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credentials_exception):
    try:
        # Payload es el mismo diccionario que es contenido por data de la funcion create_access_token
        payload = jwt.decode(token, SECRET_KEY, algorithms = [ALGORITHM])
        extracted_id: str = payload.get("user_id")

        if extracted_id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id = extracted_id)
    
    except JWTError:
        raise credentials_exception
    
    return token_data

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code = status.HTTP_401_UNAUTHORIZED, detail = f"Could not validate credentials", headers = {"WWW-Authenticate": "Bearer"})

    return verify_access_token(token, credentials_exception)
