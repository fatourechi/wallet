from sqlalchemy.orm import Session
from .repository import CodeRepository
from db import schemas
from db.redis import get_redis_handler


class CodeService:
    def __init__(self, db_session: Session) -> None:
        self.repository = CodeRepository(db_session)
        self.redis_handler = get_redis_handler()


    def create_user(self, code: schemas.CodeCreate):
        try:
            db_code = self.repository.create_code(code)
        except ValueError as e:
            raise ValueError(e)
        
        code_info = {
            "amount": db_code.amount,
            "limit": db_code.limit
        }
        if db_code.start_time:
            code_info.update({
                "start_time": db_code.start_time.timestamp(),
            })
        if db_code.expire_time:
            code_info.update({
                "expire_time": db_code.expire_time.timestamp()
            })
        self.redis_handler.set_code_info(db_code.value, code_info)
        return db_code
    
    def get_codes(self):
        return self.repository.get_codes()
    
    def get_code_by_id(self, code_id: int):
        return self.repository.get_code_by_id(code_id)
    
    def get_code_by_value(self, code_value: str):
        return self.repository.get_code_by_value(code_value)
    
    def delete_code(self, code_id: int):
        deleted_code = self.repository.delete_code_by_id(code_id)
        if deleted_code:
            self.redis_handler.delete_code(deleted_code.value)
        return deleted_code
    
    def get_code_statistic(self):
        return self.redis_handler.get_all_codes_limits()