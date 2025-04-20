# import google.generativeai as genai
# from gemini_config import get_configured_model # Or wherever get_text_model/get_multimodal_model is

import sys

# --- Import the packages/modules ---
text_chat_session_module = None
try:
    # Import the specific chat_session module from the text_chat package
    from text_chat import chat_session
    text_chat_session_module = chat_session # Store the imported module
    print("Text chat session module 'text_chat.chat_session' loaded.")
except ImportError as e:
    # This will now catch the ImportError originating from config.py
    print(f"Warning: Could not load text_chat package or chat_session module. Error: {e}", file=sys.stderr)

# Import multimodal_chat session module if available, wrap in try/except
multimodal_chat_session_module = None
try:
    from multimodal_chat import multimodal_session
    multimodal_chat_session_module = multimodal_session
    print("Multimodal chat session module 'multimodal_chat.multimodal_session' loaded.")
except ImportError as e:
    print(f"Warning: Could not load multimodal_chat package or multimodal_session module. Error: {e}", file=sys.stderr)


# --- Define the main entry point function ---
def main():
    print("Welcome to the Gemini Project Runner!")

    # --- Build available options ---
    options = []
    # Check the *session module* for the function
    if text_chat_session_module and hasattr(text_chat_session_module, 'run_text_chat'):
        options.append(("Run Text Chat Session", text_chat_session_module.run_text_chat))
    else:
         # This check is only reached if the module itself loaded but the function wasn't found on it
         if text_chat_session_module:
             print("Warning: 'run_text_chat' function not found in text_chat.chat_session module.", file=sys.stderr)


    # Check the *session module* for the function (multimodal)
    if multimodal_chat_session_module and hasattr(multimodal_chat_session_module, 'run_multimodal_chat'):
        options.append(("Run Multimodal Chat Session", multimodal_chat_session_module.run_multimodal_chat))
    else:
         if multimodal_chat_session_module:
             print("Warning: 'run_multimodal_chat' function not found in multimodal_chat.multimodal_session module.", file=sys.stderr)


    # --- Handle case with no runnable options ---
    if not options:
        print("\nNo runnable chat sessions found. Please check package imports and ensure main run functions exist within the correct modules.", file=sys.stderr)
        print("Look at the WARNING messages above for details on which packages failed to load.", file=sys.stderr) # Added hint
        return # Exit the program if nothing can be run

    # --- Display options and get user input ---
    while True: # Loop to allow running multiple sessions or handling invalid input
        print("\nAvailable options:")
        for i, (description, _) in enumerate(options):
            print(f"  {i + 1}. {description}")
        print("  q. Quit")

        choice = input("Enter the number of your choice, or 'q' to quit: ").strip().lower()

        if choice == 'q':
            print("Exiting.")
            break

        try:
            choice_index = int(choice) - 1 # Convert input to 0-based index
            if 0 <= choice_index < len(options):
                # Valid choice - get the function and run it
                description, selected_function = options[choice_index]
                print(f"\n--- Running: {description} ---")
                try:
                    selected_function() # Execute the chosen function!
                except Exception as e:
                    print(f"An error occurred while running {description}: {e}", file=sys.stderr)
                print(f"--- Finished: {description} ---")
                # After running, the loop continues, asking for the next choice
            else:
                print("Invalid number. Please try again.")
        except ValueError:
            # Handle cases where input is not a number
            print("Invalid input. Please enter a number or 'q'.")
        except Exception as e:
            print(f"An unexpected error occurred during option selection: {e}", file=sys.stderr)


if __name__ == "__main__":
    main()