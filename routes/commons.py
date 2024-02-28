import os
import google.generativeai as genai
import logging

def get_env_var(var_name):
    try:
        return os.getenv(var_name)
    except os.error as e:
        logging.error(f"Error in getting environment variable: {str(e)}")




def generate_response(KEY, PRE_PROMPT, user_prompt):
    try:
        gemini_api_key = KEY
        genai.configure(api_key=gemini_api_key)

        finall_query = PRE_PROMPT + user_prompt
        model = genai.GenerativeModel('gemini-pro')
        response = model.generate_content(finall_query)

        return response.text

    except Exception as e:
        # Log the error
        logging.error(f"Error in generate_response: {str(e)}")
        # You can customize the logging based on your requirements
        # For example, you may want to log to a file or send alerts

        # Return an appropriate error message or handle it as per your application's needs
        return "An error occurred while generating the response. Please try again later."
