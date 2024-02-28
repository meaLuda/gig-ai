import os
from typing import List
from fastapi import APIRouter, HTTPException


from .pre_prompts import (
    COVER_LETTER_FROM_JD_PROMPTS,FIT_TO_JD_PROMPTS
)
from .schema import JobsPrompt
from ..commons import get_env_var
jobwins = APIRouter()



@jobwins.post('/prompt/')
def gigwin_prompt(prompt: JobsPrompt):
    item = prompt.prompt
    return {"Response":item}