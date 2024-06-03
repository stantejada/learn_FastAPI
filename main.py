from fastapi import FastAPI
#importando los routers desde /routers/users.py and /routers/products.py
from routers import products, users
from fastapi.staticfiles import StaticFiles

app = FastAPI()

#routers 
app.include_router(products.router)
app.include_router(users.router)
#es la forma de exponer archivos estaticos (images, pdf, txt, videos etc.)
app.mount("/static", StaticFiles(directory='static'), name="static")



@app.get("/")
async def root():
    return {"url":"https://github.com/stantejada/"}



