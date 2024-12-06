from fastapi import FastAPI
from .routers import auth
from app import db

app = FastAPI()

@app.on_event("startup")
def on_startup():
    print('Table created...')
    db.create_table()

@app.get('/')
async def hello():
    return "Hello world"

app.include_router(auth.router, prefix='/auth', tags=['auth'])