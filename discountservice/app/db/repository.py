from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from .models import Code
from db import schemas

class CodeRepository:
    def __init__(self, db_session: Session) -> None:
        self.db = db_session

    def create_code(self, code: schemas.CodeCreate):
        try:
            db_code = Code(**code.model_dump())
            self.db.add(db_code)
            self.db.commit()
            self.db.refresh(db_code)
            return db_code
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Failed to create code: Code with this value already exists")


    def get_codes(self):
        return self.db.query(Code).all()
    
    def get_code_by_id(self, code_id: int):
        return self.db.query(Code).filter(Code.id == code_id).first()
    
    def get_code_by_value(self, code_value: str):
        return self.db.query(Code).filter(Code.value == code_value).first()
    
    def delete_code_by_id(self, code_id: int):
        db_code = self.db.query(Code).filter(Code.id == code_id).first()
        if db_code:
            self.db.delete(db_code)
            self.db.commit()
            return db_code