from pydantic import BaseModel

# Basemodel for the job description
class Prompt(BaseModel):
    prompt: str
    license: str
    email: str