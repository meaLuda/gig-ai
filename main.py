import os
import uvicorn
from fastapi import FastAPI
import openai


from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
import redis
from dotenv import load_dotenv,dotenv_values

load_dotenv()


# setup app and database
app = FastAPI()

# setup redis
r = redis.Redis(host='localhost',port=6379,db=0) 



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
# docker run -p 6379:6379 -it redis/redis-stack:latest

# Basemodel for the job description
class Prompt(BaseModel):
    prompt: str
    license: str
    email: str

env_dev = os.environ['DEV']
# print(env_dev)

# environment set-up must have these in your local and dev path
if  env_dev == 'True':
    env_key = os.environ['OPENAI_API_KEY']
    HOST = "176.58.111.181"
    openai.api_key = env_key

if env_dev != 'True':
    HOST ="localhost"
    config = dotenv_values(".env")
    openai.api_key = config['OPENAI_API_KEY_TEST']
    

# use your own key here
    

# Define the key for storing the count of prompts for each user license
KEY_TEMPLATE = 'prompt-count-{}-{}'

# prompts to chat with gigai
GIG_PROMPTS = """
Given a freelance job description that will start after: Respond accordingly to the following job description:
Generate a proposal or cover letter that provides a breakdown of how I will solve the tasks outlined in the given job description, 
outline any possible specific tools or processes that the I can use to complete the job, and provide a breakdown of how 
I plan to accomplish each task using the specified tools or processes, give me best practices, tools, or processes to complete the job and explain how these will be employed to achieve the best possible outcome.
Do not talk about my experience or skills. Rather focus on the tasks, tools, and processes that to be used to complete the job. make it solution oriented.
If the input is not a job description, make sure to only reply with: "Sorry, this does not look like a job description, please try again."
Respond accordingly to the following job description: \n \n
"""

# Define the limit of prompts per day per user license
PROMPT_LIMIT = 15
# PROMPT_LIMIT = 3

count = 0 # count of times the root has been called
@app.get("/")
async def root():
    global count
    # check how many times the root has been called by the user.
    count += 1
    return {"message": f"Hello World {count}"}

def get_current_date():
    return datetime.datetime.now().strftime("%Y-%m-%d")

# route for the prompt
@app.post("/api/gigai/")
async def gigai(prompt: Prompt):
    
    user_license = prompt.license
    current_date = get_current_date()
    key = KEY_TEMPLATE.format(user_license, current_date)

    # Increment the count of prompts for this user license and date
    prompt_count = r.incr(key)
    
    # print(
    #     {
    #         "user_license": user_license,
    #         "current_date": current_date,
    #         "key": key,
    #         "prompt_count": prompt_count,
    #     }
    # )

    # If the count exceeds the limit, return an error
    if prompt_count > PROMPT_LIMIT:
        return {"error": "Too many prompts today."}

    if prompt.prompt and isinstance(prompt.prompt, str) and len(prompt.prompt.strip()) > 30:
        # remove await if not working.
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt= GIG_PROMPTS + " \n \n "+prompt.prompt,
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
            return {"message": "Sorry this does not look like a job description, try again"}

# change the host here to local host.
if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=8000, reload=True,log_level="info")