from pymongo import MongoClient
from datetime import datetime
from typing import Optional

class MongoLogger:
    def __init__(self, mongo_uri: str) -> None:
        self.client = MongoClient(mongo_uri)
        self.db = self.client["transaction_logs"]
        self.collection = self.db['transactions']

    async def log_deposit_transaction(self, user_id: int, amount: float, timestamp: datetime):
        transaction_data = {
            'user_id': user_id,
            'amount': amount,
            'timestamp': timestamp
        }
        await self.collection.insert_one(transaction_data)
    
    def __parse_transaction(self, document):
        return {
            "user_id": document['user_id'],
            "amount": document['amount'],
            "timestamp": document['timestamp']
        }
    
    def __parse_transactions(self, documents):
        return [self.__parse_transaction(document) for document in documents]
    
    async def get_all_transactions(self, limit: int, skip: int = 0):
        if limit < 0:
            return []
        
        transactions = await self.collection.find().sort("timestamp", -1).skip(skip).limit(limit)
        if transactions:
            return self.__parse_transactions(transactions)
        else:
            []

    async def get_transactions_by_filter(self, user_id: Optional[int] = None , start_date: Optional[datetime] = None, end_date: Optional[datetime] = None):
        query = {"user_id": user_id}
        if user_id:
            query["user_id"] = user_id
        if start_date or end_date:
            timestamp_query = {}
            if start_date:
                timestamp_query["$gte"] = start_date
            if end_date:
                timestamp_query["$lte"] = end_date
            query["timestamp"] = timestamp_query

        transactions = await self.collection.find(query)

        if transactions:
            return self.__parse_transactions(transactions)
        else:
            return []
