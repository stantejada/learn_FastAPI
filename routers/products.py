from fastapi import APIRouter

#prefix = /route means that is not necessary to pass /route/{id} and just to pass /{id}
#tags = ["products"] means to separate different categories. see localhost/Docs to see the changes
#responses indicate that if any problems result from the operation it will return a error http 404 not found
router = APIRouter(prefix="/products",
                    tags=["products"],
                    responses={404:{"message": "No found"}})


#lista de ejemplo
lista = [f"producto {i}" for i in range(5)]


@router.get("/")
async def products():
    
    return lista


@router.get("/{id}")
async def products(id: int):
    return lista[id]