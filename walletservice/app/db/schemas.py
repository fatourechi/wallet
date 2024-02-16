from pydantic import BaseModel
from typing import Optional


class WalletBase(BaseModel):
    balance: float

class WalletCreate(WalletBase):
    user_id: Optional[int]

class Wallet(WalletBase):
    id: int
    user_id: Optional[int]
    
    class config:
        orm_mode = True

class UserBase(BaseModel):
    mobile_number: str
    name: str

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int
    wallet: Optional[Wallet] = None
    class config:
        orm_mode = True


class Deposit(BaseModel):
    mobile_number: str
    code: str