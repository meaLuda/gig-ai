from pydantic import BaseModel

# Basemodel for the job description
class GigsPrompt(BaseModel):
    prompt: str
    # license: str
    # email: str