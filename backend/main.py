from fastapi import FastAPI, Body

from database import init_db

app = FastAPI()


@app.on_event("startup")
async def on_startup():
    await init_db()


market_list = []


@app.get("/")
async def index():
    return {"message": "Hello World"}


@app.get("/login")
async def get_market():
    return market_list
