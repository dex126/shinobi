import redis.asyncio as redis

from telegram import config


states_db = redis.Redis(
    host=config.DB_HOST,
    port='6379',
    decode_responses=True,
    db=0)


users_db = redis.Redis(
    host=config.DB_HOST,
    port='6379',
    decode_responses=True,
    db=1)
