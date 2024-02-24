from fastapi import FastAPI, HTTPException
from db import schemas
from db.database import Base, engine, SessionLocal
from db.service import WalletService


Base.metadata.create_all(bind=engine)

app = FastAPI()

wallet_service = WalletService(SessionLocal())

@app.post("/wallets/", response_model=schemas.Wallet)
def create_new_wallet(wallet: schemas.WalletCreate):
    wallet, error = wallet_service.create_wallet(wallet)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return wallet

@app.get("/wallets/{wallet_id}", response_model=schemas.Wallet)
def get_single_wallet(wallet_id: int):
    wallet, error = wallet_service.get_wallet_by_wallet_id(wallet_id)
    if error:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

@app.get("/wallets/user_id/{user_id}", response_model=schemas.Wallet)
def get_single_wallet_by_user_id(user_id: int):
    wallet, error = wallet_service.get_wallet_by_user_id(user_id)
    if error:
        raise HTTPException(status_code=404, detail="Wallet not found")
    return wallet

@app.post("/wallets/deposit/")
def deposit_balance(deposit: schemas.Deposit):
    db_wallet, error = wallet_service.deposit_balance(deposit)
    if error:
        raise HTTPException(status_code=400, detail=error)
    return db_wallet
     
