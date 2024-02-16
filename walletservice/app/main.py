# userservice/app/main.py

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from db.crud import create_wallet, get_wallet_by_id, get_wallet_by_user_id, delete_wallet, \
                    deposit_balance_by_user_id
from db import schemas
from db.database import Base, engine, SessionLocal
from db.http_requests import get_user_by_id_request, log_deposit_transaction_request, \
                        get_user_by_mobile_number_request
from datetime import datetime
from db.redis import get_redis_handler
from db.logging import logger


redis_handler = get_redis_handler()

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD endpoints
@app.post("/wallets/", response_model=schemas.Wallet)
def create_new_wallet(wallet: schemas.WalletCreate, db: Session = Depends(get_db)):
    user = get_user_by_id_request(user_id=wallet.user_id)
    if not user:
        # If user does not exist, raise HTTPException with 404 Not Found error
        raise HTTPException(status_code=404, detail="User not found")
    
    return create_wallet(db, wallet)

@app.get("/wallets/{wallet_id}", response_model=schemas.Wallet)
def get_single_wallet(wallet_id: int, db: Session = Depends(get_db)):
    wallet = get_wallet_by_id(db, wallet_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

@app.get("/wallets/user_id/{user_id}", response_model=schemas.Wallet)
def get_single_wallet_by_user_id(user_id: int, db: Session = Depends(get_db)):
    wallet = get_wallet_by_user_id(db, user_id)
    if not wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

@app.delete("/wallets/{wallet_id}")
def delete_existing_wallet(wallet_id: int, db: Session = Depends(get_db)):
    deleted_wallet = delete_wallet(db, wallet_id)
    if not deleted_wallet:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return deleted_wallet

@app.post("/wallets/deposit/")
def deposit_balance(deposit: schemas.Deposit, db: Session = Depends(get_db)):
    user = get_user_by_mobile_number_request(mobile_number=deposit.mobile_number)
    if not user:
        logger.error("User not found")
        raise HTTPException(status_code=404, detail="User not found")

    code_info = redis_handler.get_code_info(code_value=deposit.code)
    if not code_info:
        raise HTTPException(status_code=404, detail="Code not found")
    
    if not code_info.get("limit"):
        raise HTTPException(status_code=404, detail="Code limit has been reached")
    
    current_time = datetime.now()
    start_time = code_info.get('start_time')
    if start_time and not (current_time > start_time):
        raise HTTPException(status_code=403, detail="Code is not yet valid")
    
    expire_time = code_info.get('expire_time')
    if expire_time and not (current_time < expire_time):
        raise HTTPException(status_code=403, detail="Code has been expired")
    
    db_wallet = deposit_balance_by_user_id(db, user.get("id"), code_info.get("amount"))
    if not db_wallet:
        raise HTTPException(status_code=404, detail="Wallet not found for user")
    redis_handler.decrease_code_limit(deposit.code)
    log_deposit_transaction_request(user_id=user.get("id"), amount=code_info.get("amount"))
    return db_wallet
