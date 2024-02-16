from sqlalchemy.orm import Session
from . import models
from . import schemas


def create_code(db: Session, code: schemas.CodeCreate):
    db_code = models.Code(**code.dict())
    db.add(db_code)
    db.commit()
    db.refresh(db_code)
    return db_code

def get_codes(db: Session):
    return db.query(models.Code).all()

def get_code_by_id(db: Session, code_id: int):
    return db.query(models.Code).filter(models.Code.id == code_id).first()

def get_code_by_code_value(db: Session, code_value: str):
    return db.query(models.Code).filter(models.Code.value == code_value).first()

def delete_code_by_id(db: Session, code_id: int):
    db_code = db.query(models.Code).filter(models.Code.id == code_id).first()
    if db_code:
        db.delete(db_code)
        db.commit()
        return db_code
    