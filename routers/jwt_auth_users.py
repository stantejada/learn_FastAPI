from fastapi import APIRouter, Depends, status, HTTPException
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer
from jose import jwt, JWTError
from passlib.context import CryptContext
from datetime import datetime, timedelta


ALGORITHM = "HS256"
ACCESS_TOKEN_DURATION = 1
SECRET = "3d37b5fee607e00be956937e3803f55732a0563e0ef5dfae7d345de6f51818da"

router = APIRouter()

oauth2 = OAuth2PasswordBearer(tokenUrl='login')

crypt = CryptContext(schemes=["bcrypt"])


class User(BaseModel):                                                                                                 
    email: str
    disable: bool

class UserDB(User):
    password: str

users_db = {
    "mouredev":{
        "username": "mouredev",
        "name": "Brais Moure",
        "email": "braismoure@moure.dev",
        "disable": False,
        "password": "$2a$12$.sO7nZnqTa5a98WjzF8Bw.yDT3uOZEoDqkAvF6M1SHzvG3yV6IoXe",
    },
    "mouredev2":{
        "username": "mouredev2",
        "name": "Brais Moure 2",
        "email": "braismoure2@moure.dev",
        "disable": True,
        "password": "$2a$12$Jz0pP4hpBKzi46v0m7e6OOTEUeRXMebxWSzGy8yPvZ4IjNrqOJhxG",
    },
}

def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])


async def auth_user(token:str = Depends(oauth2)):

    exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="User is not authorized!",
                    headers={"WWW-Authenticate":"Bearer"})

    try:
        username = jwt.decode(token, SECRET, algorithms=[ALGORITHM]).get("sub")
        if username is None:
            raise exception
    except JWTError:
        raise exception

    return search_user(username)


async def current_user(user: str = Depends(auth_user)):
    
    if user.disable:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, 
                    detail="Users is disabled")
    return user 



@router.post("/login")
async def login(form: OAuth2PasswordRequestForm = Depends()):
    user_db = users_db.get(form.username)
    if not user_db:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="User is not correct!")
    user = search_user_db(form.username)
    
    if not crypt.verify(form.password, user.password):
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is not correct!")


    access_token = {"sub":user.username,
     "exp":datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_DURATION)}

    return {"access_token": jwt.encode(access_token, algorithm=ALGORITHM, key=SECRET), "token_type":"JWT"}



@router.get("/users/me")
async def me(user:User = Depends(current_user)):
    return user
