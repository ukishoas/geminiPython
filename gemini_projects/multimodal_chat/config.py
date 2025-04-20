from gemini_configuration import get_model, configure_api_key # Import both

def get_multimodal_model():
    # Ensure API key is configured
    configure_api_key()

    # Define specific generation config for multimodal if needed
    multimodal_gen_config = { # Example config, adjust as needed
      "temperature": 0.4,
      "max_output_tokens": 4000,
      # ... other multimodal-specific settings
    }
     # Call get_model with the *specific* multimodal model name
    model = get_model(model_name="gemini-pro-vision", generation_config=multimodal_gen_config)
    return model