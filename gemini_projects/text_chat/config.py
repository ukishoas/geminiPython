from gemini_configuration import get_model, configure_api_key

def get_text_model():
    configure_api_key()

    text_gen_config = {
      "temperature": 0.7,
      "max_output_tokens": 4000,
      # ... other text-specific settings
    }
     # Call get_model with the *specific* text model name
    model = get_model(model_name="gemini-2.5-flash-preview-04-17", generation_config=text_gen_config)
    return model