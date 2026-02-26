import os
from openai import OpenAI
import openai

# Function to test connection to OpenAI using the provided API key
def test_openai_api_key(api_key):
    """
    Returns a tuple (bool, str):
        - bool: True if the connection is successful, False otherwise.
        - str: A success message or error description.
    """
    try:
        # Initialize OpenAI API key
        clientGPT = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))

        if clientGPT.api_key is None:
            raise ValueError("OpenAI API key not found. Set it in the environment variable 'OPENAI_API_KEY'")
        

        # Make a lightweight request to test the key (e.g., list available models)
        response = clientGPT.chat.completions.create(
            model="gpt-4o-mini",  # Use the updated model name as needed
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You only answer in ironic haikus of AI and Software Engineering."
                    )
                },
                {
                    "role": "user",
                    "content": f"How is it going?"
                }
            ],
            temperature=0.5  # Adjust to control creativity
        )
        
        # Check if the response contains expected data
        if response:
            print("****** testing api key:")
            print(response.choices[0].message.content.strip())
            return True, "API key is valid and connected successfully."
        else:
            return False, "Unexpected response structure while testing the API key."
    except Exception as e:
        # Handle errors gracefully and provide feedback
        return False, f"Error testing API key: {e}"

# Function to summarize text using OpenAI API
def summarize_text(text):
    """
    Summarizes the given text using OpenAI API.
    """
    print("OpenAI Summarization")
    #print(f"\tOriginal text: {text}")

    if not text or len(text.strip()) < 5:
        return text  # Return input if it's None or too short
    try:
        # Initialize OpenAI API key 
        # Replace with your actual OpenAI API key
        clientGPT = OpenAI(api_key=os.environ.get("OPENAI_API_KEY"))
        if clientGPT.api_key is None:
            raise ValueError("OpenAI API key not found. Set it in the environment variable 'OPENAI_API_KEY'")
        
        # Request summary from the OpenAI API
        response = clientGPT.chat.completions.create(
            model="gpt-4o-mini",  # Use the updated model name as needed
            messages=[
                {
                    "role": "system",
                    "content": (
                        "You are an assistant that provides a concise summary of text followed by key points. "
                        "Start with a brief overview, then list the details as bullet points."
                    )
                },
                {
                    "role": "user",
                    "content": f"Keep all of the formatting relatively the same. Here is some text that needs cleaning and summarizing:\n\n{text}"
                }
            ],
            temperature=0.5  # Adjust to control creativity
        )
        # Extract and return the structured response
        
        summary = response.choices[0].message.content.strip()
        print("\n\n\n\n\-----------------------------SUMMary\n\n\n",flush=True)
        print(summary,flush=True)
        print(response,flush=True)
        print("\n\n\n\n\-----------------------------end\n\n\n",flush=True)

        #print(f"\tGenerated, Summarized Response:\n{summary}")
        return summary
    except Exception as e:
        print(f"\tError during summarization: {e}")
        return None
    
# Function to generate OpenAI embeddings for new queries
def get_openai_embedding(text):
    try:
        # Generate embedding using OpenAI API with the correct syntax
        response = openai.embeddings.create(
            model="text-embedding-ada-002",
            input=text
        )
        # Correct access to embedding data in the response object
        embedding = response.data[0].embedding
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None