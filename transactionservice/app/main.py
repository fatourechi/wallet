# userservice/app/main.py

from fastapi import FastAPI, Query
import os 
from db.mongo import MongoLogger
from db import schemas
from datetime import datetime, timedelta
from typing import Optional, List


MONGO_SERVER = os.getenv("MONGO_SERVER", "localhost")
MONGO_URI = f'mongodb://{MONGO_SERVER}:27017/'
mongo_logger = MongoLogger(MONGO_URI)

app = FastAPI()


@app.post("/transactions/")
async def log_transaction(transaction: schemas.Transaction):
    timestamp = datetime.now()
    mongo_logger.log_deposit_transaction(transaction.user_id, transaction.amount, timestamp)
    return {"message": "Transaction logged successfully"}

@app.get("/transactions/")
async def get_all_transactions():
    transactions = mongo_logger.get_all_transactions()
    return {"transactions": transactions}

@app.get("/transactions/user/{user_id}")
async def get_transactions_by_user(user_id: int):
    transactions = mongo_logger.get_transactions_by_user(user_id)
    return {"transactions": transactions}

@app.get("/transactions/date_range/")
async def get_transactions_by_date_range(
    start_date: Optional[datetime] = Query(None, description="Start date of the range"),
    end_date: Optional[datetime] = Query(None, description="End date of the range")
):
    if not start_date:
        start_date = datetime.now() - timedelta(days=7)  # Default to last 7 days
    if not end_date:
        end_date = datetime.now()
    transactions = mongo_logger.get_transactions_by_date_range(start_date, end_date)
    return {"transactions": transactions}