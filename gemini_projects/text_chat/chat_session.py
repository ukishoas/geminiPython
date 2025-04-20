from .config import get_text_model
import sys # For potential error output

def run_text_chat():
    """Contains the main logic for the text chat session."""
    print("--- Starting Text Chat Logic ---")
    try:
        model = get_text_model()
        print("Text model loaded.")

        chat = model.start_chat(history=[])
        print("\nStart chatting! Type 'quit' to end.")
        while True:
            user_input = input("You: ")
            if user_input.lower() == 'quit':
                break # Exit the loop if user types 'quit'
        
            try:
                response = chat.send_message(user_input)
                print(f"Bot: {response.text}")
            except Exception as e:
                print(f"Error sending message: {e}", file=sys.stderr)

    except Exception as e:
        print(f"An error occurred during text chat logic: {e}", file=sys.stderr)

    print("--- Text Chat Logic Finished ---") # This line is reached when the loop finishes or an error occurs