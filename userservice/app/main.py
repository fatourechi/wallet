# userservice/app/main.py

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from db.crud import create_user, get_user, update_user_by_user_id, delete_user, \
    get_user_by_mobile_number, get_users, update_user_by_mobile_number
from db import schemas
from db.database import Base, engine, SessionLocal
import requests

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD endpoints
@app.post("/users/", response_model=schemas.User)
def create_new_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    try:
        user = create_user(db, user)
    except Exception as e:
        raise HTTPException(status_code=400, detail="mobile number is duplicated")

    wallet_data = {"user_id": user.id, "balance": 0}
    wallet_creation_response = requests.post("http://walletservice/wallets/", json=wallet_data)

    if wallet_creation_response.status_code == 200:
        return user
    else:
        # If wallet creation failed, handle the error accordingly
        raise HTTPException(status_code=500, detail="Failed to create wallet for user")

@app.get("/users/", response_model=List[schemas.User])
def get_all_users(db: Session = Depends(get_db)):
    return get_users(db)

@app.get("/users/{user_id}", response_model=schemas.User)
def get_single_user(user_id: int, db: Session = Depends(get_db)):
    user = get_user(db, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.get("/users/mobile_number/{mobile_number}", response_model=schemas.User)
def get_single_user_by_mobile_number(mobile_number: str, db: Session = Depends(get_db)):
    user = get_user_by_mobile_number(db, mobile_number)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

@app.put("/users/{user_id}", response_model=schemas.User)
def update_existing_user_by_user_id(user_id: int, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = update_user_by_user_id(db, user_id, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.put("/users/{mobile_number}", response_model=schemas.User)
def update_existing_user_by_mobile_number(mobile_number: str, user: schemas.UserUpdate, db: Session = Depends(get_db)):
    updated_user = update_user_by_mobile_number(db, mobile_number, user)
    if not updated_user:
        raise HTTPException(status_code=404, detail="User not found")
    return updated_user

@app.delete("/users/{user_id}", response_model=schemas.User)
def delete_existing_user(user_id: int, db: Session = Depends(get_db)):
    deleted_user = delete_user(db, user_id)
    if not deleted_user:
        raise HTTPException(status_code=404, detail="User not found")
    return deleted_user


