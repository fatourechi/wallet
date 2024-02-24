import requests
from datetime import datetime


def make_request(url, method, json=None):
    response = requests.request(method, url, json=json)
    if response.status_code == 200:
        return response.json()
    else:
        raise Exception(f"Error making request to {url}, error: {response.text}")
    
def get_user_by_id_request(user_id: int):
    try:
        return make_request(f"http://userservice/users/{user_id}", "GET")
    except Exception as e:
        print(str(e))

def get_user_by_mobile_number_request(mobile_number: str):
    try:
        return make_request(f"http://userservice/users/mobile_number/{mobile_number}", "GET")
    except Exception as e:
        print(str(e))

def log_deposit_transaction_request(user_id: int, code: str, mobile_number: str, amount: float):
    try:
        data = {
            "user_id": user_id,
            "code": code,
            "mobile_number": mobile_number,
            "amount": amount,
        }
        make_request(f"http://transactionservice/transactions", "POST", json=data)
    except Exception as e:
        print(str(e))