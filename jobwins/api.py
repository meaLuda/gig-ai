import os
from typing import List
from fastapi import APIRouter, HTTPException
import openai
import sys
sys.path.append("..")


jobwins = APIRouter()

# connection to redis
from redis_connect import redis_client_
from pre_prompts import FIT_TO_JD_PROMPTS, COVER_LETTER_FROM_JD_PROMPTS
from .models import Prompt
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
@jobwins.post('/')
async def resume_to_jd(prompt: Prompt):
    prompt_count = redis_client_.incr("key-from-jobwins")
     # Check if the user has reached the prompt limit
    if prompt_count > PROMPT_LIMIT:
        raise HTTPException(status_code=400, detail='Prompt limit reached')

    # send to openai api

    if prompt.selectedOption == "My Fit To Job Description":
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt= FIT_TO_JD_PROMPTS + " \n \n " + prompt.jobDescription + " \n \n "+ prompt.mySkills + " \n \n "+ prompt.workHistory,
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1
        )
    
    if prompt.selectedOption == "My Work History":
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt= COVER_LETTER_FROM_JD_PROMPTS + " \n \n " + prompt.jobDescription + " \n \n "+ prompt.mySkills + " \n \n "+ prompt.workHistory,
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1
        )

    # Your code to handle the prompt goes here
    # ...
    return {"message": response.choices[0].text}
    return {
        "JobWinsTest":"Success",
        "Environemnt loaded":f"ENV VARIABLE LOADED {get_env_var('OPENAI_API_KEY_TEST')} ====> FROM JOBWINS"
    }