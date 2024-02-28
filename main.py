import os
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# other api's
from dotenv import load_dotenv
# load all env variables to the system
load_dotenv()



app = FastAPI()

origins = [
    "*", # allow all origins
    "176.58.111.181"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# local
from routes.gigwins.api import gigwins as gw
from routes.jobwins.api import jobwins as jw
from routes.commons import get_env_var

app.include_router(gw,prefix='/api/v1/gigwins', tags=['Gig Wins AI ~ API'])
app.include_router(jw,prefix='/api/v1/jobwins', tags=['Job Wins AI ~ API'])



env_dev = get_env_var('DEV')




# change host on ~ environment 
if  env_dev == 'True':
    HOST = "176.58.111.181"

if env_dev != 'True':
    HOST ='0.0.0.0'

if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=8000, reload=True,log_level="info")