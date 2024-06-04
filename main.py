from fastapi import FastAPI
#importando los routers desde /routers/users.py and /routers/products.py
from routers import products, users, jwt_auth_users, basic_auth_users, users_db
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#routers 
app.include_router(products.router)
app.include_router(users.router)
app.include_router(basic_auth_users.router)
app.include_router(jwt_auth_users.router)
app.include_router(users_db.router)


#es la forma de exponer archivos estaticos (images, pdf, txt, videos etc.)
app.mount("/static", StaticFiles(directory='static'), name="static")



@app.get("/")
async def root():
    return {"url":"https://github.com/stantejada/"}



