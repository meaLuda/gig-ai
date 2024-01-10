import os
import uvicorn
from fastapi import FastAPI
import openai

from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import datetime
import redis
from dotenv import load_dotenv,dotenv_values
from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

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
HUGGINGFACEHUB_API_TOKEN = os.environ["HUGGINGFACEHUB_API_TOKEN"] 
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
async def gigai():
    try:
        question = f"""
        Given a freelance job description that will start after: Respond accordingly to the following job description:
        Generate a proposal or cover letter that provides a breakdown of how I will solve the tasks outlined in the given job description, 
        outline any possible specific tools or processes that the I can use to complete the job, and provide a breakdown of how 
        I plan to accomplish each task using the specified tools or processes, give me best practices, tools, or processes to complete the job and explain how these will be employed to achieve the best possible outcome.
        Do not talk about my experience or skills. Rather focus on the tasks, tools, and processes that to be used to complete the job. make it solution oriented.
        If the input is not a job description, make sure to only reply with: "Sorry, this does not look like a job description, please try again."
        """
        
        template = """Question: {question}
            Answer: Let's think step by step.
        """
        # See https://huggingface.co/models?pipeline_tag=text-generation&sort=downloads for some other options
        # Prompt template to the llm
        repo_id = "google/flan-t5-xxl"
        prompt =PromptTemplate(template=template, input_variables=["question"])

        llm = HuggingFaceHub(
            repo_id=repo_id,
            model_kwargs={"tempreture":0.5,"max_lenght":1000}
        )
        llm_chain =  LLMChain(prompt=prompt,llm=llm)
        a = llm_chain.run(question)
        return {"message": a}
    except Exception as e:
        return {"message": "Sorry this does not look like a job description, try again"}

# change the host here to local host.
if __name__ == "__main__":
    uvicorn.run("main:app", host=HOST, port=8000, reload=True,log_level="info")