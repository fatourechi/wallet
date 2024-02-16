from sqlalchemy.orm import Session
from . import models, schemas

def create_wallet(db: Session, wallet: schemas.WalletCreate):
    db_wallet = models.Wallet(**wallet.dict())
    db.add(db_wallet)
    db.commit()
    db.refresh(db_wallet)
    return db_wallet

def get_wallet_by_id(db: Session, wallet_id: int):
    return db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()

def get_wallet_by_user_id(db: Session, user_id: int):
    return db.query(models.Wallet).filter(models.Wallet.user_id == user_id).first()

def delete_wallet(db: Session, wallet_id: int):
    db_wallet = db.query(models.Wallet).filter(models.Wallet.id == wallet_id).first()
    if db_wallet:
        db.delete(db_wallet)
        db.commit()
    return db_wallet

def deposit_balance_by_user_id(db: Session, user_id: int, amount: float):
    db_wallet = db.query(models.Wallet).filter(models.Wallet.user_id == user_id).first()
    if db_wallet:
        db_wallet.balance += amount
        db.commit()
        db.refresh(db_wallet)
        return db_wallet
