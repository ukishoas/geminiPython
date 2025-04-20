# your_gemini_projects/multimodal_chat/multimodal_session.py
import google.generativeai as genai
import os
# Import the function to get the configured multimodal model
from .config import get_multimodal_model

def run_multimodal_chat():
    """
    Starts an interactive chat session allowing text and file input.
    """
    try:
        model = get_multimodal_model() # Get the model configured for multimodal

        # Note: Multimodal chat history can be tricky.
        # The model might remember previous text turns, but re-sending files
        # from previous turns isn't automatically handled by `send_message` history.
        # For simplicity, we start a new chat session and include text + file
        # in a single message for each turn where a file is provided.
        # If you need persistent multimodal history, you might need to manually
        # manage the `history` list with appropriate `genai.types.Content` objects.
        chat_session = model.start_chat(history=[])

        print("\nMultimodal Chatbot started! Type 'quit' to exit.")
        print("Enter text prompt first, then optionally a file path.")
        print("-" * 40)

        while True:
            user_text_input = input("You (Text): ")

            if user_text_input.lower() == 'quit':
                print("Goodbye!")
                break

            # Optional: Ask for a file path
            file_path_input = input("Enter file path (or press Enter to skip): ")

            content_parts = []

            # Add text part if provided
            if user_text_input.strip():
                content_parts.append(user_text_input)
            elif not file_path_input.strip(): # If no text and no file, prompt again
                 print("Please enter either text or a file path.")
                 print("-" * 40)
                 continue

            # Add file part(s) if a path is provided
            if file_path_input.strip():
                # Basic check if file exists
                if not os.path.exists(file_path_input):
                    print(f"Error: File not found at '{file_path_input}'. Please try again.")
                    print("-" * 40)
                    continue # Skip this turn and ask again

                try:
                    # Upload the file
                    # Note: Uploaded files are temporary. For longer interactions,
                    # you might need to re-upload or manage file lifetimes.
                    # The default duration is usually sufficient for one turn.
                    print(f"Uploading file: {file_path_input}...")
                    uploaded_file = genai.upload_file(path=file_path_input,
                                                       display_name=os.path.basename(file_path_input))
                    print(f"Uploaded file: {uploaded_file.uri}")
                    content_parts.append(uploaded_file)

                    # Wait for file to become usable by the model
                    # A small delay might be helpful, or use genai.get_file() status check
                    import time
                    time.sleep(1) # Simple delay, consider more robust checking if needed

                except Exception as e:
                    print(f"Error uploading file: {e}")
                    print("-" * 40)
                    continue # Skip this turn if file upload fails

            # Send the content (text and/or file(s)) to the model
            try:
                # Send the list of parts
                response = chat_session.send_message(content_parts)

                # Print the model's response
                print("Gemini:", response.text)

            except Exception as e:
                print(f"An error occurred during the API call: {e}")
                # Handle specific errors like content filtering here if needed
                # e.g., print(e.response.prompt_feedback)

            finally:
                 # Clean up the uploaded file (optional but good practice for temporary files)
                 # This often requires checking the file's state first
                 # For this simple script, relying on the automatic expiry might be okay
                 # but for more robust apps, manage file deletion.
                 if 'uploaded_file' in locals():
                     try:
                         # Check file status before deleting
                         # file_status = genai.get_file(uploaded_file.name).state
                         # if file_status == 'ACTIVE': # Or other states where deletion is safe
                         #     genai.delete_file(uploaded_file.name)
                         #     print(f"Cleaned up temporary file: {uploaded_file.display_name}")
                         pass # Skipping explicit delete for simplicity in this example
                     except Exception as cleanup_e:
                          print(f"Error during file cleanup: {cleanup_e}")


            print("-" * 40)

    except ValueError as e:
        print(f"Setup failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during setup or chat: {e}")

# --- Run the multimodal chat session when this script is executed ---
if __name__ == "__main__":
    run_multimodal_chat()