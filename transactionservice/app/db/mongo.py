from pymongo import MongoClient
from datetime import datetime


class MongoLogger:
    def __init__(self, mongo_uri: str) -> None:
        self.client = MongoClient(mongo_uri)
        self.db = self.client["transaction_logs"]
        self.collection = self.db['transactions']

    def log_deposit_transaction(self, user_id: int, amount: float, timestamp: datetime):
        transaction_data = {
            'user_id': user_id,
            'amount': amount,
            'timestamp': timestamp
        }
        self.collection.insert_one(transaction_data)
    
    def __parse_transaction(self, document):
        return {
            "user_id": document['user_id'],
            "amount": document['amount'],
            "timestamp": document['timestamp']
        }
    
    def __parse_transactions(self, documents):
        return [self.__parse_transaction(document) for document in documents]
    
    def get_all_transactions(self):
        transactions = self.collection.find()
        if transactions:
            return self.__parse_transactions(transactions)
        else:
            []

    def get_transactions_by_user(self, user_id):
        transactions = self.collection.find({"user_id": user_id})
        if transactions:
            return self.__parse_transactions(transactions)
        else:
            return []

    def get_transactions_by_date_range(self, start_date, end_date):
        transactions = self.collection.find({"timestamp": {"$gte": start_date, "$lte": end_date}})
        if transactions:
            return self.__parse_transactions(transactions)
        else:
            return []