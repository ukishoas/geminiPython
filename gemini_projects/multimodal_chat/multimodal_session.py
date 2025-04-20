import google.generativeai as genai
import os
import mimetypes
import time
import sys # Make sure sys is imported for error output

# Assuming get_multimodal_model now correctly uses gemini_config.get_model
# and specifies a multimodal model name like 'gemini-pro-vision' or 'gemini-1.5-flash-latest'
from .config import get_multimodal_model

# Define a list of MIME types that are generally supported by Gemini multimodal models
# This is not exhaustive but covers common cases (images, PDF, plain text, CSV)
SUPPORTED_MIME_TYPES = [
    'image/jpeg',
    'image/png',
    'image/gif',
    'image/webp',
    'application/pdf',
    'text/plain',
    'text/csv',
    'text/tab-separated-values',
]

def get_file_part(file_path: str):
    """Reads a file, determines mime type, and prepares it as a file part for the API."""
    if not os.path.isfile(file_path):
        print(f"Error: '{file_path}' is not a file.", file=sys.stderr)
        return None

    try:
        # --- Determine MIME type using mimetypes ---
        mime_type, _ = mimetypes.guess_type(file_path)

        # Fallback/Correction for common types if guess_type fails or is wrong
        if mime_type is None:
            file_extension = os.path.splitext(file_path)[1].lower()
            if file_extension == '.csv':
                mime_type = 'text/csv'
            elif file_extension == '.txt':
                mime_type = 'text/plain'
            elif file_extension in ['.jpg', '.jpeg']:
                mime_type = 'image/jpeg'
            elif file_extension == '.png':
                mime_type = 'image/png'
            # Add other fallbacks if necessary

        # --- Validate MIME type against supported list ---
        if mime_type not in SUPPORTED_MIME_TYPES:
            print(f"Error: File type '{mime_type}' for '{file_path}' is not supported by the model.", file=sys.stderr)
            print(f"Supported types include: {', '.join(SUPPORTED_MIME_TYPES)}", file=sys.stderr)
            return None

        # --- Upload the file using genai.upload_file ---
        # The display_name is optional but good practice
        display_name = os.path.basename(file_path)
        # Use the determined mime_type
        print(f"Uploading file: {display_name}...")
        uploaded_file = genai.upload_file(path=file_path,
                                           display_name=display_name,
                                           mime_type=mime_type) # Pass the determined MIME type here!
        print(f"Uploaded file URI: {uploaded_file.uri}")

        # IMPORTANT: In a production app, you should poll uploaded_file.state
        # until it is 'COMPLETED' before using it in send_message.
        # A simple sleep is used here for demonstration, but it's not reliable.
        # Consider using uploaded_file.state and a loop with time.sleep()
        # Or catching specific errors if the file isn't ready.
        # For CSVs/Text, the upload is usually fast, but large images/PDFs can take time.
        print("Waiting for file to be ready (simple sleep)...")
        time.sleep(5) # Increased sleep duration as 1 second might not be enough


        # You could optionally check the state here:
        # while uploaded_file.state.name == 'PROCESSING':
        #    time.sleep(1)
        #    uploaded_file = genai.get_file(uploaded_file.name) # Refresh file state
        # if uploaded_file.state.name != 'COMPLETED':
        #    print(f"Error: File upload did not complete. State: {uploaded_file.state.name}", file=sys.stderr)
        #    # Delete the failed upload
        #    try: uploaded_file.delete()
        #    except: pass # Ignore delete errors during failure
        #    return None


        # The uploaded_file object itself is a valid Part for send_message
        return uploaded_file

    except FileNotFoundError:
        print(f"Error: File not found at '{file_path}'.", file=sys.stderr)
        return None
    except Exception as e:
        print(f"Error reading, uploading, or preparing file '{file_path}': {e}", file=sys.stderr)
        return None


# --- Main chat function ---
def run_multimodal_chat():
    """
    Starts an interactive chat session allowing text and file input at the start,
    then continues with text-only follow-up questions.
    """
    try:
        model = get_multimodal_model() # Get the configured model

        # Check if model loading failed
        if model is None:
             print("Failed to load multimodal model. Cannot start chat.", file=sys.stderr)
             return

        print("\nMultimodal Chatbot started! Type 'quit' to exit at any text prompt.")
        print("First, provide the file you want to discuss, then your initial question.")
        print("-" * 40)

        # --- Phase 1: Initial File Upload and First Message ---

        uploaded_file_part = None # Variable to store the uploaded file object
        file_path_input = input("Enter path to the file for discussion (or press Enter to skip): ").strip()

        if file_path_input:
            uploaded_file_part = get_file_part(file_path_input)
            # If file upload failed, uploaded_file_part will be None.
            # The helper prints error messages.

        # --- Get the initial text prompt ---
        print("\nNow, enter your initial question about the file (or just press Enter if you only attached a file):")
        initial_user_text = input("You (Initial Question): ").strip()

        # --- Build the initial message parts ---
        initial_content_parts = []
        if initial_user_text:
            initial_content_parts.append(initial_user_text)
        if uploaded_file_part: # Only add the file part if upload was successful
            initial_content_parts.append(uploaded_file_part)

        # --- Validate Initial Input ---
        # You need at least some text or a successfully uploaded file to start
        if not initial_content_parts:
            print("No initial text or valid file provided. Exiting chat.", file=sys.stderr)
            # No file to clean up if uploaded_file_part is None
            return

        # --- Start Chat and Send First Message ---
        print("\n--- Sending Initial Message to Gemini ---")
        chat_session = model.start_chat(history=[]) # Start the chat session

        try:
            # Send the initial message containing both text (if any) and the file (if any)
            response = chat_session.send_message(initial_content_parts)
            print("Gemini:", response.text)

        except Exception as e:
            print(f"An error occurred sending initial message: {e}", file=sys.stderr)
            print("Chat session could not start. Exiting.", file=sys.stderr)
            # If initial send failed, we should clean up the file if it was uploaded
            if uploaded_file_part:
                print("Attempting to clean up uploaded file...", file=sys.stderr)
                try:
                    # uploaded_file_part.delete() # Uncomment if you want to delete failed uploads
                    print(f"Would delete failed uploaded file: {uploaded_file_part.uri}", file=sys.stderr)
                except Exception as cleanup_e:
                     print(f"Error during failed file cleanup: {cleanup_e}", file=sys.stderr)
            return # Exit the function if the first message fails

        # --- Phase 2: Interactive Follow-up Conversation (Text Only) ---

        print("\n--- Continue Chat (File is part of history) ---")
        print("Ask follow-up questions. Type 'quit' to exit.")
        print("-" * 40)

        while True:
            # Only prompt for text input in subsequent turns
            user_text_input = input("You: ").strip()

            if user_text_input.lower() == 'quit':
                print("Goodbye!")
                break

            if not user_text_input:
                print("Please enter some text.", file=sys.stderr)
                continue # Don't send empty messages

            # Send ONLY the text input; the file is already in the chat history
            try:
                # Pass just the text string or a list containing just the text string
                response = chat_session.send_message(user_text_input) # Or [user_text_input]
                print("Gemini:", response.text)

            except Exception as e:
                print(f"An error occurred during the API call: {e}", file=sys.stderr)
                # Decide error handling - maybe break the loop or continue?
                # For now, let's just print the error and continue the loop.

            print("-" * 40)

        # --- Cleanup after the conversation loop finishes ---
        print("\nChat session ended. Cleaning up uploaded file...")
        # Check if a file was successfully uploaded initially and clean it up
        if uploaded_file_part:
            try:
                 # You can optionally delete the file from Google's servers
                 # after the session or when you're done with it.
                 print(f"Would delete file: {uploaded_file_part.uri}")
                 # uploaded_file_part.delete() # Uncomment this line if you want to delete files
                 # print(f"Deleted file: {uploaded_file_part.uri}")
            except Exception as cleanup_e:
                 print(f"Error cleaning up file {uploaded_file_part.uri}: {cleanup_e}", file=sys.stderr)
        print("Cleanup finished.")


    # --- Error Handling for Setup (Outer try block) ---
    # These catch errors BEFORE the loop starts (e.g., model loading failed)
    except ValueError as e: # Catch specific setup errors like missing API key
        print(f"Setup failed (ValueError): {e}", file=sys.stderr)
    except Exception as e: # Catch other unexpected setup errors
        print(f"An unexpected error occurred during initial setup: {e}", file=sys.stderr)

# --- Standard Python entry point ---
if __name__ == "__main__":
    # Ensure API is configured before running the chat session if not done elsewhere
    # Assuming configure_api_key exists in gemini_config and handles the global setting
    try:
        get_multimodal_model() # Configure API key at startup
        run_multimodal_chat()
    except ImportError:
        print("Error: Could not import configure_api_key from gemini_config.", file=sys.stderr)
    except ValueError as e:
         print(f"API Configuration Error: {e}", file=sys.stderr)
    except Exception as e:
         print(f"An error occurred during initial setup or execution: {e}", file=sys.stderr)