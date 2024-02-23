# userservice/app/main.py

from fastapi import FastAPI, HTTPException, Depends
from typing import List
from db import schemas
from db.database import Base, engine, SessionLocal
from db.redis import get_redis_handler
from db.service import CodeService

redis_handler = get_redis_handler()

Base.metadata.create_all(bind=engine)

app = FastAPI()

code_service = CodeService(db_session=SessionLocal())

@app.post("/codes/", response_model=schemas.Code)
def create_new_code(code:  schemas.CodeCreate):
    try:
        user = code_service.create_user(code)
        return user
    except Exception as e:
        raise HTTPException(status_code=400, detail="Code is duplicated")

@app.get("/codes/", response_model=List[schemas.Code])
def get_all_codes():
    return code_service.get_codes()

@app.get("/codes/{code_id}", response_model=schemas.Code)
def get_single_code(code_id: int):
    code = code_service.get_code_by_id(code_id)
    if not code:
        raise HTTPException(status_code=404, detail="Code not found")
    return code

@app.get("/codes/value/{code_value}", response_model=schemas.Code)
def get_single_code_by_code_value(code_value: str):
    code = code_service.get_code_by_value(code_value)
    if not code:
        raise HTTPException(status_code=404, detail="Code not found")
    return code

@app.delete("/codes/{code_id}", response_model=schemas.Code)
def delete_existing_code(code_id: int):
    deleted_code = code_service.delete_code(code_id)
    if not deleted_code:
        raise HTTPException(status_code=404, detail="Code not found")
    return deleted_code

@app.get("/codes/statistic/")
def get_code_statistic():
    return code_service.get_code_statistic()