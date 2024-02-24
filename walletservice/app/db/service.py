from .repository import WalletRepository, UserRepository
from sqlalchemy.orm import Session
from db import schemas
from .redis import get_redis_handler
from datetime import datetime
from .http_requests import log_deposit_transaction_request

class WalletService:
    def __init__(self, db_session: Session) -> None:
        self.wallet_repository = WalletRepository(db_session)
        self.user_repository = UserRepository(db_session)
        self.redis_handler = get_redis_handler()

    def create_wallet(self, wallet: schemas.WalletCreate):
        user = self.user_repository.get_user_by_id(wallet.user_id)
        if not user:
            return None, "user not found"
        
        try:
            wallet = self.wallet_repository.create_wallet(wallet.model_dump())
            return wallet, ""
        except Exception as e:
            return None, str(e)
    
    def get_wallet_by_wallet_id(self, wallet_id: int):
        wallet = self.wallet_repository.get_wallet_by_id(wallet_id)
        if not wallet:
            return None, "wallet not found"
        return wallet , ""
    
    def get_wallet_by_user_id(self, user_id: int):
        wallet = self.wallet_repository.get_wallet_by_user_id(user_id)
        if not wallet: 
            return None, "wallet not found"
        return wallet, ""
    
    def deposit_balance(self, deposit: schemas.Deposit):
        user = self.user_repository.get_user_by_mobile_number(deposit.mobile_number)
        if not user:
            return None, "user not found"
        
        code_info = self.redis_handler.get_code_info(deposit.code)

        if not code_info:
            return None, "user does not existed"
        
        if not code_info.get("limit"):
            return None, "Code limit reachs it's limit"
        
        current_time = datetime.now()

        start_time = code_info.get('start_time')
        if start_time and not (current_time > start_time):
            return None, "Code is not yet valid"
        
        expire_time = code_info.get('expire_time')
        if expire_time and not (current_time < expire_time):
            return None, "Code has been expired"
        
        try:
            db_wallet = self.wallet_repository.deposit_balance_by_user_id(user_id=user.get("id"),
                                                                      amount=code_info.get("amount"))
        except Exception as e:
            return None, str(e)
        self.redis_handler.decrease_code_limit(deposit.code)
        log_deposit_transaction_request(user_id=user.get("id"), amount=code_info.get("amount"))
        return db_wallet, ""