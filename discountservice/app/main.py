# userservice/app/main.py

from fastapi import FastAPI, HTTPException, Depends
from sqlalchemy.orm import Session
from typing import List
from db.crud import create_code, get_codes, get_code_by_code_value, get_code_by_id, delete_code_by_id
from db import schemas
from db.database import Base, engine, SessionLocal
from db.redis import get_redis_handler

redis_handler = get_redis_handler()

Base.metadata.create_all(bind=engine)

app = FastAPI()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD endpoints
@app.post("/codes/", response_model=schemas.Code)
def create_new_user(code: schemas.CodeCreate, db: Session = Depends(get_db)):
    db_code = create_code(db, code)
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
    redis_handler.set_code_info(db_code.value, code_info)
    return db_code

@app.get("/codes/", response_model=List[schemas.Code])
def get_all_codes(db: Session = Depends(get_db)):
    return get_codes(db)

@app.get("/codes/{code_id}", response_model=schemas.Code)
def get_single_code(code_id: int, db: Session = Depends(get_db)):
    code = get_code_by_id(db, code_id)
    if not code:
        raise HTTPException(status_code=404, detail="Code not found")
    return code

@app.get("/codes/value/{code_value}", response_model=schemas.Code)
def get_single_code_by_code_value(code_value: str, db: Session = Depends(get_db)):
    code = get_code_by_code_value(db, code_value)
    if not code:
        raise HTTPException(status_code=404, detail="Code not found")
    return code

@app.delete("/codes/{code_id}", response_model=schemas.Code)
def delete_existing_code(code_id: int, db: Session = Depends(get_db)):
    deleted_code = delete_code_by_id(db, code_id)
    if not deleted_code:
        raise HTTPException(status_code=404, detail="Code not found")
    redis_handler.delete_code(deleted_code.value)
    return deleted_code

@app.get("/codes/statistic/")
def get_code_statistic():
    return redis_handler.get_all_codes_limits()