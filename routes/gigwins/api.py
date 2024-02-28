import os
import datetime
from typing import List
from fastapi import APIRouter, HTTPException



from ..commons import get_env_var,generate_response
from .pre_prompts import GIG_PRE_PROMPTS
from .schema import GigsPrompt


gigwins = APIRouter()

GOOGLE_API_KEY=get_env_var('GEMINI_KEY')


@gigwins.post('/prompt/')
def gigwin_prompt(prompt: GigsPrompt):
    item = prompt.prompt
    q_a = generate_response(KEY=get_env_var('GEMINI_KEY',),PRE_PROMPT=GIG_PRE_PROMPTS,user_prompt=item)
    return {"Response":q_a}