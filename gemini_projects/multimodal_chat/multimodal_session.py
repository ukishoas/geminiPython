import google.generativeai as genai
import os
from .config import get_multimodal_model

def run_multimodal_chat():
    """
    Starts an interactive chat session allowing text and file input.
    """
    try:
        model = get_multimodal_model()
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
                    print(f"Uploading file: {file_path_input}...")
                    uploaded_file = genai.upload_file(path=file_path_input,
                                                       display_name=os.path.basename(file_path_input))
                    print(f"Uploaded file: {uploaded_file.uri}")
                    content_parts.append(uploaded_file)

                    import time
                    time.sleep(1) # Simple delay, consider more robust checking if needed

                except Exception as e:
                    print(f"Error uploading file: {e}")
                    print("-" * 40)
                    continue # Skip this turn if file upload fails

            try:
                response = chat_session.send_message(content_parts)

                print("Gemini:", response.text)

            except Exception as e:
                print(f"An error occurred during the API call: {e}")
                
            finally:
                 if 'uploaded_file' in locals():
                     try:
                         pass # Skipping explicit delete for simplicity in this example
                     except Exception as cleanup_e:
                          print(f"Error during file cleanup: {cleanup_e}")


            print("-" * 40)

    except ValueError as e:
        print(f"Setup failed: {e}")
    except Exception as e:
        print(f"An unexpected error occurred during setup or chat: {e}")

if __name__ == "__main__":
    run_multimodal_chat()