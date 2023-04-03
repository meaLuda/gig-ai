from pydantic import BaseModel

# Basemodel for the job description
class Prompt(BaseModel):
    selectedOption: str
    jobDescription: str
    mySkills: str
    workHistory: str
    email: str
    supportCode: str
   