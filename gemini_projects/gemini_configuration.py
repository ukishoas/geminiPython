import os
import google.generativeai as genai
from dotenv import load_dotenv

_api_key_configured = False # Use a flag to configure only once

def configure_api_key():
    """Loads env vars and configures the Gemini API (only once)."""
    global _api_key_configured
    if _api_key_configured:
        return

    load_dotenv()
    api_key = os.environ.get("GEMINI_API_KEY")

    if not api_key:
        raise ValueError("GEMINI_API_KEY environment variable not set...")

    genai.configure(api_key=api_key)
    _api_key_configured = True
    print("Gemini API configured successfully.") # Print success here


def get_model(model_name: str, generation_config: dict):
    """
    Returns a configured GenerativeModel instance for a specific model name.
    Assumes configure_api_key() has been called.
    """
    # Ensure API key is configured before getting a model
    # configure_api_key() # You could call it here too, but calling once in app start is cleaner

    try:
        model = genai.GenerativeModel(
          model_name=model_name,
          generation_config=generation_config,
        )
        print(f"Successfully created model instance: {model_name}")
        return model

    except Exception as e:
        print(f"Error creating the GenerativeModel '{model_name}': {e}")
        raise

# You would then call configure_api_key() once in chat_app.py or similar startup code.
# You would *not* have genai.configure() inside get_model() if it takes model_name.