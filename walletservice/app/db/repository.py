from .models import User, Wallet
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from db import schemas

class WalletRepository:
    def __init__(self, db_session: Session) -> None:
        self.db = db_session

    def create_wallet(self, wallet: schemas.Wallet):
        try:
            db_wallet = Wallet(**wallet.model_dump())
            self.db.add(db_wallet)
            self.db.commit()
            self.db.refresh(db_wallet)
            return db_wallet
        except IntegrityError as e:
            self.db.rollback()
            raise ValueError("Failed to create wallet: Wallet with for this user already exists")
        
    def get_wallet_by_id(self, wallet_id: int):
        return self.db.query(Wallet).filter(Wallet.id == wallet_id).first()
    
    def get_wallet_by_user_id(self, user_id: int):
        return self.db.query(Wallet).filter(Wallet.user_id == user_id).first()
    
    def deposit_balance_by_user_id(self, user_id: int, amount: float):
        try:
            db_wallet = self.db.query(Wallet).filter(Wallet.user_id == user_id).first()
            if not db_wallet:
                raise ValueError("Wallet not found for user")
            
            db_wallet.balance += amount
            self.db.commit()
            self.db.refresh(db_wallet)

            return db_wallet
        except ValueError as value_error:
            self.db.rollback()
            raise value_error
        except Exception as e:
            self.db.rollback()
            raise Exception(f"Unexcepted error occured: {e}")
        

class UserRepository:
    def __init__(self, db_session: Session) -> None:
        self.db = db_session

    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_mobile_number(self, mobile_number: str):
        return self.db.query(User).filter(User.mobile_number == mobile_number).first()
    
