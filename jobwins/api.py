import os
from typing import List
from fastapi import APIRouter, HTTPException
import sys
sys.path.append("..")


jobwins = APIRouter()

# connection to redis
from redisclientconnect import RedisClient as RC

redis_client_jobwins = RC()


def get_env_var(var_name):
    return os.getenv(var_name)

# test route
@jobwins.get('/')
async def test_jobwins():
    print(get_env_var('OPENAI_API_KEY_TEST'))
    cech = redis_client_jobwins.incr("key-from-jobwins")
    print(cech)
    return {
        "JobWinsTest":"Success",
        "Environemnt loaded":f"ENV VARIABLE LOADED {get_env_var('OPENAI_API_KEY_TEST')} ====> FROM JOBWINS"
    }