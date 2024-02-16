from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from .database import Base


class Wallet(Base):
    __tablename__ = "wallets"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), unique=True, nullable=True)
    balance = Column(Float, default=0)   

    user = relationship("User", back_populates="wallet")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    mobile_number = Column(String, unique=True, index=True, nullable=True)
    name = Column(String, nullable=False)

    wallet = relationship("Wallet", back_populates="user")

