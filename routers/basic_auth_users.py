from fastapi import FastAPI, Depends, HTTPException, status
from pydantic import BaseModel
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm


router = FastAPI()

oauth2 = OAuth2PasswordBearer(tokenUrl='login')


class User(BaseModel):
    username: str
    name: str
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
        "password": "12345",
    },
    "mouredev2":{
        "username": "mouredev2",
        "name": "Brais Moure 2",
        "email": "braismoure2@moure.dev",
        "disable": True,
        "password": "54321",
    },
}

def search_user_db(username:str):
    if username in users_db:
        return UserDB(**users_db[username])

def search_user(username:str):
    if username in users_db:
        return User(**users_db[username])


async def current_user(token: str = Depends(oauth2)):
    user = search_user(token)
    if not user:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, 
                    detail="User is not authorized!",
                    headers={"WWW-Authenticate":"Bearer"})
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
    if not form.password == user.password:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Password is not correct!")

    return {"access_token": user.username, "token_type":"bearer"}

@router.get("/users/me")
async def me(user:User = Depends(current_user)):
    return user