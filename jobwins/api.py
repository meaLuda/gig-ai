import os
from typing import List
from fastapi import APIRouter, HTTPException
import openai
import sys
sys.path.append("..")


jobwins = APIRouter()

# connection to redis
from redisclientconnect import redis_client_

def get_env_var(var_name):
    return os.getenv(var_name)

env_dev = get_env_var('DEV')

# on production ~ live kwa server
if  env_dev == 'True':
    # Define the limit of prompts per day per user license
    PROMPT_LIMIT = 15
    openai.api_key = get_env_var('OPENAI_API_KEY')

# on development
if env_dev != 'True':
    PROMPT_LIMIT = 3
    openai.api_key = get_env_var('OPENAI_API_KEY_TEST')

# Define the key for storing the count of prompts for each user license
KEY_TEMPLATE = 'prompt-count-{}-{}'




# test route
@jobwins.get('/')
async def test_jobwins():
    print(get_env_var('OPENAI_API_KEY_TEST'))
    prompt_count = redis_client_.incr("key-from-jobwins")
     # Check if the user has reached the prompt limit
    if prompt_count > PROMPT_LIMIT:
        raise HTTPException(status_code=400, detail='Prompt limit reached')
    print(prompt_count)
    
    return {
        "JobWinsTest":"Success",
        "Environemnt loaded":f"ENV VARIABLE LOADED {get_env_var('OPENAI_API_KEY_TEST')} ====> FROM JOBWINS"
    }