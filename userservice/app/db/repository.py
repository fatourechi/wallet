from .models import User
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from db import schemas


class UserRepository:
    def __init__(self, db_session: Session) -> None:
        self.db = db_session
    
    def create_user(self, user: schemas.UserCreate):
        try:
            db_user = User(**user.model_dump())
            self.db.add(db_user)
            self.db.commit()
            self.db.refresh(db_user)
            return db_user
        except IntegrityError:
            self.db.rollback()
            raise ValueError("Failed to create user: User with this mobile number already exists")
    
    def get_users(self):
        return self.db.query(User).all()
    
    def get_user_by_id(self, user_id: int):
        return self.db.query(User).filter(User.id == user_id).first()
    
    def get_user_by_mobile_number(self, mobile_number: str):
        return self.db.query(User).filter(User.mobile_number == mobile_number).first()
    
    def delete_user_by_id(self, user_id: int):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        if db_user:
            self.db.delete(db_user)
            self.db.commit()
            return db_user

    def update_user_by_user_id(self, user_id: int, user: User):
        try:
            db_user = self.db.query(User).filter(User.id == user_id).first()
            if not db_user:
                raise ValueError('No user found')

            for attr, value in user.dict().items():
                setattr(db_user, attr, value)
                
            self.db.add(db_user)
            try:
                self.db.commit()
            except IntegrityError as e:
                self.db.rollback()
                raise ValueError('Integrity Error: {}'.format(str(e)))
            
            return db_user
        except ValueError as ve:
            self.db.rollback()
            raise ve
        except Exception as ex:
            self.db.rollback()
            raise Exception('Unexpected error occurred: {}'.format(str(ex)))
    
    def update_user_by_mobile_number(self, mobile_number: str, user: User):
        try:
            db_user = self.db.query(User).filter(User.mobile_number == mobile_number).first()
            if not db_user:
                raise ValueError('No user found')
            
            for attr, value in user.dict().items():
                setattr(db_user, attr, value)
                
            self.db.add(db_user)
            try:
                self.db.commit()
            except IntegrityError as e:
                self.db.rollback()
                raise ValueError('Integrity Error: {}'.format(str(e)))
            
            return db_user
        except ValueError as ve:
            self.db.rollback()
            raise ve
        except Exception as ex:
            self.db.rollback()
            raise Exception('Unexpected error occurred: {}'.format(str(ex)))
    