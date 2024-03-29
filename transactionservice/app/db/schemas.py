from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class Transaction(BaseModel):
    user_id: int
    amount: float
    code: str
    mobile_number: str

class GetTransaction(BaseModel):
    user_id: int
    start_date: Optional[datetime] = None
    end_date: Optional[datetime] = None