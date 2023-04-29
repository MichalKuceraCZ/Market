from fastapi import FastAPI, Body, status

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
async def login():
    return login
