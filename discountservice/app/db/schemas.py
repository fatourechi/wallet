from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CodeBase(BaseModel):
    value: str
    amount: float
    limit: int
    start_time: Optional[datetime]
    expire_time: Optional[datetime]

class CodeCreate(CodeBase):
    pass 

class Code(CodeBase):
    id: int

    class Config:
        orm_mode = True