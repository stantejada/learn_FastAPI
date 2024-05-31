from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"url":"https://github.com/stantejada/"}



