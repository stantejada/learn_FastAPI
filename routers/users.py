from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

router = APIRouter(tags=["users"])

#Entidad user
class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list =[
    User(id=1, name="Brais", surname="Moure", url="https://moure.dev", age=35),
    User(id=2, name="Moure", surname="Dev", url="https://mouredev.com", age=35),
    User(id=3, name="Haakon", surname="Dahlberg", url="https://haakon.com", age=33),
]



@router.get('/users')
async def users():
    return users_list

#peticion por medio de path/id
@router.get("/user/{id}")
async def user(id: int):
    return search_user(id)

#peticion por medio de query ejemplo: /path/?id=1 <-- query
@router.get("/user/")
async def user(id: int):
    return search_user(id)

#crear un usuario
@router.post("/user/", response_model=User,status_code=201)
async def user(user:User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=204, detail="User already exists!")
        
    else:
        users_list.append(user)
    return user

#actualizar un usuario
@router.put("/user/")
async def user(user: User):
    found = False
    for index, user_saved in enumerate(users_list):
        if user_saved.id == user.id:
            users_list[index] = user
            found = True
    
    if not found:
        return {"Error":"User not updated!"}

#borrar un usuario
@router.delete("/user/{id}")
async def user(id:int):
    found = False
    for index,user_saved in enumerate(users_list):
        if user_saved.id == id:
            del users_list[index]  
            found = True

    if not found:
        return {"Error":"User not Exists!"}
    

def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"Error":"User not found!"}

