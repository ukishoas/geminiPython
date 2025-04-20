from gemini_configuration import get_model, configure_api_key

def get_multimodal_model():
    configure_api_key()

    multimodal_gen_config = { 
      "temperature": 0.4,
      "max_output_tokens": 4000,
      # ... other multimodal-specific settings
    }
    model = get_model(model_name="gemini-1.5-flash", generation_config=multimodal_gen_config)
    return model