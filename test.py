import os
import uvicorn
from fastapi import FastAPI
import openai


from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
import redis

# other api's
from gigwins.api import gigwins as gw
from jobwins.api import jobwins as jw
from dotenv import load_dotenv

# load all env variables to the system
load_dotenv()

app = FastAPI()

app.include_router(gw,prefix='/api/v1/gigwins', tags=['Gig Wins AI ~ API'])
app.include_router(jw,prefix='/api/v1/jobwins', tags=['Job Wins AI ~ API'])


if __name__ == "__main__":
    uvicorn.run("test:app", host="localhost", port=8000, reload=True,log_level="info")