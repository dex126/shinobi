import redis.asyncio as redis

from telegram import config


ITER_BATCH_SIZE = 500 


states_db = redis.Redis(
    host=config.DB_HOST,
    port='6379',
    decode_responses=True,
    db=0)
