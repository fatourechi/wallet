# userservice/app/main.py

from fastapi import FastAPI
from db import schemas
from db.service import TransactionService

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
async def get_transactions_by_filter(get_transaction: schemas.GetTransaction):
    transactions = await transaction_service.get_transactions(user_id=get_transaction.user_id,
                                                              start_date=get_transaction.start_date,
                                                              end_date=get_transaction.end_date)
    return {"transactions": transactions}
