import redis
import os
from datetime import datetime


class RedisClient:
    def __init__(self, host, port):
        self.redis_client = redis.Redis(host=host, port=port)

    def acquire_lock(self, resource_identifier: str):
        lock_key = f"LOCK:{resource_identifier}"
        success = self.redis_client.setnx(lock_key, "locked")
        if success:
            self.redis_client.expire(lock_key, 30)
            return True
        else:
            return False

    def release_lock(self, resource_identifier: str):
        lock_key = f"LOCK:{resource_identifier}"
        if self.redis_client.delete(lock_key):
            return True
        else:
            raise RuntimeError('Failed to release lock')
        
    def set_code_info(self, code_value: str, info: dict):
        self.redis_client.hmset(f"CODE||{code_value}", info)

    def get_code_info(self, code_value: str):
        code_info = self.redis_client.hgetall(f"CODE||{code_value}")
        if code_info:
            return {
                "amount": float(code_info[b'amount'].decode("utf-8")) if code_info.get(b'amount') else 0,
                "limit": int(code_info[b'limit'].decode("utf-8")) if code_info.get(b'limit') else 0,
                "start_time": datetime.fromtimestamp(float(code_info[b'start_time'].decode("utf-8"))) if code_info.get(b'start_time') else None,
                "expire_time": datetime.fromtimestamp(float(code_info[b'expire_time'].decode("utf-8"))) if code_info.get(b'expire_time') else None,
            }
        return None

    def decrease_code_limit(self, code_value: str):
        self.redis_client.hincrby(f"CODE||{code_value}", "limit", -1)
        
    def delete_code(self, code_value: str):
        self.redis_client.delete(f"CODE||{code_value}")

    def get_code_limit(self, code_value: str):
        return self.redis_client.hget(f"CODE||{code_value}", "limit")
    
    def get_all_codes_limits(self):
        keys = self.redis_client.keys("CODE||*")

        code_limits = {}
        for key in keys:
            key = key.decode("utf-8")
            code_value = key.split("||")[1]
            code_limits[code_value] = self.get_code_limit(code_value)
        return code_limits

REDIS_SERVER = os.getenv("REDIS_SERVER", "localhost")
REDIS_PORT = os.getenv("REDIS_PORT", 6379)


def get_redis_handler():
    return RedisClient(REDIS_SERVER, REDIS_PORT)
