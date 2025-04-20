# your_gemini_projects/api_setup.py
import os
import google.generativeai as genai
from dotenv import load_dotenv

def configure_gemini_api():
    """
    Loads environment variables and configures the Gemini API.
    Raises a ValueError if the API key is not found.
    """
    load_dotenv() # Load variables from the .env file

    api_key = os.environ.get("GEMINI_API_KEY")

    if api_key:
    # Maybe set it globally? Or just print success?
        print("Gemini API configured successfully.")
    # IT NEEDS TO RETURN THE KEY IF get_text_model expects it as a return value
    else:
        print("Error: GOOGLE_API_KEY not found in environment or .env file.")
    # It might return None, which would cause the error later
    return api_key # Or maybe it doesn't have a return None, implicitly returns None

# You can call this function immediately when the file is imported,
# or have modules call it themselves. Let's have modules call it.
# configure_gemini_api()