from .mongo import MongoLogger
from db import schemas
from typing import Optional
from datetime import datetime, timedelta
import os

MONGO_SERVER = os.getenv("MONGO_SERVER", "localhost")
MONGO_URI = f'mongodb://{MONGO_SERVER}:27017/'

class TransactionService:
    def __init__(self):
        self.mongo_logger = MongoLogger(MONGO_URI)
    
    async def log_transaction(self, transaction: schemas.Transaction):
        await self.mongo_logger.log_deposit_transaction(user_id=transaction.user_id, 
                                                        amount=transaction.amount,
                                                        code=transaction.code,
                                                        mobile_number=transaction.mobile_number,
                                                        timestamp=datetime.now())

    async def get_transactions(self, user_id: Optional[int] = None, start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
        return await self.mongo_logger.get_transactions_by_filter(user_id=user_id,
                                                                  start_date=start_date,
                                                                  end_date=end_date)
    async def get_all_transactions(self, limit: int = 10, skip: int = 0):
        return await self.mongo_logger.get_all_transactions(limit=limit, skip=skip)
    
    async def get_transactions_by_code(self, code):
        return await self.mongo_logger.get_transactions_by_code(code=code)