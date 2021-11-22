# app/main.py

from fastapi import FastAPI

from app.db import database, User

app = FastAPI(title="Fitapka")


@app.get("/")
async def read_root():
    return await User.objects.all()


@app.post("/users/", response_model=User)
async def create_user(user: User):
    return await user.save()


@app.on_event("startup")
async def startup():
    if not database.is_connected:
        await database.connect()


@app.on_event("shutdown")
async def shutdown():
    if database.is_connected:
        await database.disconnect()
