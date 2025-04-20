from gemini_configuration import get_model, configure_api_key # Import both

def get_text_model():
    # Ensure API key is configured (safe to call multiple times with the flag)
    configure_api_key()

    # Define specific generation config for text if needed, or reuse a default
    text_gen_config = { # Example config, adjust as needed
      "temperature": 0.7,
      "max_output_tokens": 4000,
      # ... other text-specific settings
    }
     # Call get_model with the *specific* text model name
    model = get_model(model_name="gemini-2.5-flash-preview-04-17", generation_config=text_gen_config)
    return model