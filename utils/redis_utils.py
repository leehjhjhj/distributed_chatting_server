from decouple import config
from redis import Redis
import logging

def get_redis_connection(db_select: int):
    REDIS_HOST=config('REDIS_HOST')
    redis_con = Redis(host=REDIS_HOST, port=6379, db=db_select)
    try:
        if not redis_con.ping():
            return None
    except Exception as e:
        logging.error('REDIS ERROR:', e)
        return None

    return redis_con
