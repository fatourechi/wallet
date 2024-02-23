# userservice/app/main.py

from fastapi import FastAPI, HTTPException
from typing import List
from db import schemas
from db.database import Base, engine, SessionLocal
from db.service import UserService

Base.metadata.create_all(bind=engine)

app = FastAPI()


user_service = UserService(db_session=SessionLocal())

# CRUD endpoints
@app.post("/users/", response_model=schemas.User)
def create_new_user(user: schemas.UserCreate):
    user , error = user_service.create_user(user)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return user

@app.get("/users/", response_model=List[schemas.User])
def get_all_users():
    return user_service.get_users()

@app.get("/users/{user_id}", response_model=schemas.User)
def get_single_user(user_id: int):
    user, error = user_service.get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail=error)
    return user

@app.get("/users/mobile_number/{mobile_number}", response_model=schemas.User)
def get_single_user_by_mobile_number(mobile_number: str):
    user, error = user_service.get_user_by_mobile_number(mobile_number)
    if not user:
        raise HTTPException(status_code=404, detail=error)
    return user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_existing_user_by_user_id(user_id: int, user: schemas.UserUpdate):
    updated_user, error = user_service.update_user(user_id, user)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return updated_user

@app.put("/users/{mobile_number}", response_model=schemas.User)
def update_existing_user_by_mobile_number(mobile_number: str, user: schemas.UserUpdate):
    updated_user = user_service.update_user_by_mobile_number(mobile_number, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_existing_user(user_id: int):
    deleted_user = user_service.delete_user(user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user


