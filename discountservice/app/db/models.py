from sqlalchemy import Boolean, Column, ForeignKey, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from .database import Base
from datetime import datetime


class Code(Base):
    __tablename__ = "codes"

    id = Column(Integer, primary_key=True, index=True)
    value = Column(String, unique=True, index=True, nullable=False)
    amount = Column(Float, nullable=False)
    limit = Column(Integer, nullable=False)
    start_time = Column(DateTime, default=datetime.now)
    expire_time = Column(DateTime)