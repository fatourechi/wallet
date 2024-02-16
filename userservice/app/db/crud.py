from sqlalchemy.orm import Session
from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()

def get_user_by_mobile_number(db: Session, mobile_number: str):
    return db.query(models.User).filter(models.User.mobile_number == mobile_number).first()

def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(mobile_number=user.mobile_number, name=user.name)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def update_user_by_user_id(db: Session, user_id: int, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        for attr, value in user.dict().items():
            setattr(db_user, attr, value)
        db.add(db_user)
        db.commit()
    return db_user

def update_user_by_mobile_number(db: Session, mobile_number: str, user: schemas.UserUpdate):
    db_user = db.query(models.User).filter(models.User.mobile_number == mobile_number).first()
    if db_user:
        for attr, value in user.dict().items():
            setattr(db_user, attr, value)
        db.add(db_user)
        db.commit()
    return db_user

def delete_user(db: Session, user_id: int):
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if db_user:
        db.delete(db_user)
        db.commit()
    return db_user

