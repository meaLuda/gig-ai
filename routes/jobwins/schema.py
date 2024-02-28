from pydantic import BaseModel

# Basemodel for the job description
class JobsPrompt(BaseModel):
    prompt: str
    # license: str
    # email: str