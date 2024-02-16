from pydantic import BaseModel


class UserBase(BaseModel):
    mobile_number: str
    name: str

class UserCreate(UserBase):
    pass

class UserUpdate(UserBase):
    pass

class User(UserBase):
    id: int

    class config:
        orm_mode = True