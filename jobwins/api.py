import os
from typing import List
from fastapi import APIRouter, HTTPException
import openai
import sys
import datetime

sys.path.append("..")

# connection to redis
from redis_connect import redis_client_
from pre_prompts import FIT_TO_JD_PROMPTS, COVER_LETTER_FROM_JD_PROMPTS
from .models import Prompt

jobwins = APIRouter()

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
@jobwins.post('/prompt/')
def resume_to_jd(prompt: Prompt):
    user_license = prompt.supportCode
    current_date = get_current_date()

    # Define the key for storing the count of prompts for each user license
    key = KEY_TEMPLATE.format(user_license, current_date)

    prompt_count = redis_client_.incr(F"jwk-{key}")
    
    # Check if the user has reached the prompt limit
    if prompt_count > PROMPT_LIMIT:
        return {"error": "Too many prompts today."}

    # send to openai api
    # if no option selected return error
    if prompt.selectedOption == "":
        return {"message": "Please select an option"}


    if prompt.selectedOption == "summarize-applicability":
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt= FIT_TO_JD_PROMPTS + " \n \n " + prompt.jobDescription + " \n \n "+ prompt.mySkills + " \n \n "+ prompt.workHistory,
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1
        )
        return {"message": response.choices[0].text}
    
    if prompt.selectedOption == "cover-letter":
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt= COVER_LETTER_FROM_JD_PROMPTS + " \n \n " + prompt.jobDescription + " \n \n "+ prompt.mySkills + " \n \n "+ prompt.workHistory,
            temperature=0.7,
            max_tokens=1000,
            top_p=1,
            frequency_penalty=1,
            presence_penalty=1
        )

        return {"message": response.choices[0].text}

    # if both options are not in the prompt return error
    if prompt.selectedOption != "summarize-applicability" and prompt.selectedOption != "cover-letter":
        return {"message": "Please select an option"}
    