import os
import datetime
import redis
from typing import List
from fastapi import APIRouter, HTTPException
import sys
sys.path.append("..")
# code imports 
from .models import Prompt

gigwins = APIRouter()

# connection to redis
from redisclientconnect import RedisClient as RC

redis_client_gigwins = RC()

def get_env_var(var_name):
    return os.getenv(var_name)

# test route
@gigwins.get('/')
async def test_gigwins():

    return {
        "GigwinsTest":"Success",
        "Environemnt loaded":f"ENV VARIABLE LOADED {get_env_var('OPENAI_API_KEY_TEST')} ====> FROM GigWINS"
    }


# Test prompt
@gigwins.post('/prompt/')
async def test_prompt(prompt:Prompt):
    cech = redis_client_gigwins.incr("key-from-gigwins")
    print(cech)
    return prompt