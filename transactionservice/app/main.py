# userservice/app/main.py

from fastapi import FastAPI, Query
from db import schemas
from db.service import TransactionService
from datetime import datetime

app = FastAPI()

transaction_service = TransactionService()

@app.post("/transactions/")
async def log_transaction(transaction: schemas.Transaction):
    await transaction_service.log_transaction(transaction)
    return {"message": "Transaction logged successfully"}

@app.get("/transactions/")
async def get_all_transactions(skip: int = 0, limit: int = 10):
    transactions = await transaction_service.get_all_transactions(skip=skip, limit=limit)
    return {"transactions": transactions}

@app.get("/transactions/user")
async def get_transactions_by_filter(user_id: int = Query(..., gt=0),
                                     start_date: datetime = Query(None),
                                     end_date: datetime = Query(None)):
    transactions = await transaction_service.get_transactions(user_id=user_id,
                                                              start_date=start_date,
                                                              end_date=end_date)
    return {"transactions": transactions}

@app.get("/transactions/code")
async def get_transactions_by_code(code: str):
    transactions = await transaction_service.get_transactions_by_code(code=code)
    return {"transactions": transactions}

