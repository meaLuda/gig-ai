# Pre-prompts are used to help the AI understand the context of the prompt.

# gig api pre-prompts
GIG_PROMPTS = """
Given a freelance job description that will start after: Respond accordingly to the following job description:
Generate a proposal or cover letter that provides a breakdown of how I will solve the tasks outlined in the given job description, 
outline any possible specific tools or processes that the I can use to complete the job, and provide a breakdown of how 
I plan to accomplish each task using the specified tools or processes, give me best practices, tools, or processes to complete the job and explain how these will be employed to achieve the best possible outcome.
Do not talk about my experience or skills. Rather focus on the tasks, tools, and processes that to be used to complete the job. make it solution oriented.
If the input is not a job description, make sure to only reply with: "Sorry, this does not look like a job description, please try again."
Respond accordingly to the following job description: \n \n
"""

# jobwins api pre-prompts
FIT_TO_JD_PROMPTS = """ 
Given a job description, my skills and experience, give a summary of how my skills and experience match the previously given job description:
Give the summary in points form
Show negatives and positives I need to improve on
If these does not seam like a job description, reply with: "Sorry, this does not look like a job description, please try again."
"""

COVER_LETTER_FROM_JD_PROMPTS = """
Given a job description, skills and experience that I have, respond with a brief cover letter:
"""