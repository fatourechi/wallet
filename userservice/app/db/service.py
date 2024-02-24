from .repository import UserRepository
from sqlalchemy.orm import Session
from db import schemas
import requests


class UserService:
    def __init__(self, db_session: Session):
        self.repository = UserRepository(db_session)
    
    def create_user(self, user: schemas.UserCreate):
        try:
            user = self.repository.create_user(user)
        except Exception as e:
            return None, str(e)

        wallet_data = {"user_id": user.id, "balance": 0}
        wallet_creation_response = requests.post("http://walletservice/wallets/", json=wallet_data)

        if wallet_creation_response.status_code == 200:
            return user, ""
        else:
            self.repository.delete_user_by_id(user.id) # delete created user because wallet creation failed
            return None, "Failed to create wallet for user"
        
    def get_users(self):
        return self.repository.get_users()
    
    def get_user_by_id(self, user_id: int):
        user = self.repository.get_user_by_id(user_id)
        if not user:
            return user, "User not found"
        return user, ""
        
    
    def get_user_by_mobile_number(self, mobile_number: str):
        user = self.repository.get_user_by_mobile_number(mobile_number)
        if not user:
            return user, "User not found"
        return user, ""
    
    def delete_user(self, user_id: int):
        return self.repository.delete_user_by_id(user_id)
    
    def update_user(self, user_id: int, user: schemas.UserUpdate):
        try:
            user = self.repository.update_user_by_user_id(user_id, user)
            return user, ""
        except Exception as e:
            return None, str(e)
    
    def update_user_by_mobile_number(self, mobile_number: str, user: schemas.UserUpdate):
        try:
            user = self.repository.update_user_by_mobile_number(mobile_number, user)
            return user, ""
        except Exception as e:
            return None, str(e)
            