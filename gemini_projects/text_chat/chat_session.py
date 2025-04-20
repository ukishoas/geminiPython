# text_chat/chat_session.py

from .config import get_text_model
import sys # For potential error output

def run_text_chat():
    """Contains the main logic for the text chat session."""
    print("--- Starting Text Chat Logic ---")
    try:
        model = get_text_model() # Calls your get_text_model from config.py
        print("Text model loaded.")

        # >>> THIS IS WHERE YOUR INTERACTIVE CHAT LOOP NEEDS TO GO <<<
        # Currently, your code likely ends here or just has comments/placeholders.
        # You need to add the code that actually talks to the model based on user input.

        # Example of what should be here:
        chat = model.start_chat(history=[]) # Start a chat session with the model
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
                # Decide how to handle send errors - maybe break, maybe continue

    except Exception as e:
        # This catches errors during model loading or *within* the loop if not handled internally
        print(f"An error occurred during text chat logic: {e}", file=sys.stderr)

    print("--- Text Chat Logic Finished ---") # This line is reached when the loop finishes or an error occurs