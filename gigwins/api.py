import os
import datetime
import openai
from typing import List
from fastapi import APIRouter, HTTPException
import sys
sys.path.append("..")


# ~infile code imports 
from .models import Prompt
# connection to redis
from redis_connect import redis_client_

# ~ pre-prompt imports
from pre_prompts import GIG_PROMPTS

gigwins = APIRouter()


def get_env_var(var_name):
    """
        ### Get environment variables from OS.
    """
    return os.getenv(var_name)

def get_current_date():
    """
        ### Get current date in format Year Month Date.
    """
    return datetime.datetime.now().strftime("%Y-%m-%d")


# get environment variable dev or production
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
@gigwins.get('/')
async def test_gigwins():
    return {
        "GigwinsTest":"Success",
    }


# Test prompt
@gigwins.post('/prompt/')
async def test_prompt(prompt:Prompt):
    
    user_license = prompt.license
    current_date = get_current_date()

    # Define the key for storing the count of prompts for each user license
    key = KEY_TEMPLATE.format(user_license, current_date)

    prompt_count = redis_client_.get(f"key-from-gigwins-{key}")
    
    if prompt_count is None:
        prompt_count = 0
    else:
        prompt_count = int(prompt_count)

    # Check if the user has reached the prompt limit
    if prompt_count >= PROMPT_LIMIT:
        return {"error": "Too many prompts today."}
    else:
        redis_client_.incr(f"gwk-{key}")
    
        # Check if the prompt is a job description ~ i presume should be greater than 30 characters.
        if prompt.prompt and isinstance(prompt.prompt, str) and len(prompt.prompt.strip()) > 30:
            # remove await if not working.
            response = openai.Completion.create(
                model="text-davinci-003",
                prompt= GIG_PROMPTS + " \n \n "+ prompt.prompt,
                temperature=0.7,
                max_tokens=1000,
                top_p=1,
                frequency_penalty=1,
                presence_penalty=1
            )

            # Your code to handle the prompt goes here
            # ...
            return {"message": response.choices[0].text}
        else:
            return {"message": "Sorry this does not look like a job description , try again"}
