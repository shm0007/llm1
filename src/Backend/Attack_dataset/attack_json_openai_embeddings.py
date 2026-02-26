import openai
import os
from dotenv import load_dotenv
import json

# Load environment variables from a .env file (for API keys)
load_dotenv()
openai.api_key = os.getenv('OPENAI_API_KEY')  # Set OpenAI API key

class GenerateEmbeddings:
    def __init__(self):
        self.cleaned_data_file = "cleaned_attack_data.txt"  # Input file
        self.output_file = "openai_attack_embeddings.json"  # Output file
        self.embeddings_data = []  # List to store data with embeddings

        # Check if the cleaned data file exists
        if not os.path.exists(self.cleaned_data_file):
            print(f"Cleaned data file not found: {self.cleaned_data_file}")
            return

        print("Starting embedding creation...")

        # Process cleaned data
        cleaned_data = self._read_cleaned_data()

        # Generate embeddings
        for entry in cleaned_data:
            print(f"Generating embedding for ID: {entry['id']} - Name: {entry['name']}")
            embedding = self.get_openai_embedding(f"{entry['name']} {entry['description']}")

            if embedding:
                print(f"Embedding for ID: {entry['id']} - Name: {entry['name']}: {embedding[:5]}... [truncated]")
                entry["embedding"] = embedding
                self.embeddings_data.append(entry)

        # Save embeddings to a JSON file
        self._save_embeddings_to_json()

    def _read_cleaned_data(self):
        # Read and parse the cleaned .txt file
        cleaned_data = []
        with open(self.cleaned_data_file, 'r') as file:
            entry = {}
            for line in file:
                line = line.strip()
                if line.startswith("File:"):
                    entry["file"] = line.replace("File: ", "")
                elif line.startswith("ID:"):
                    entry["id"] = line.replace("ID: ", "")
                elif line.startswith("Type:"):
                    entry["type"] = line.replace("Type: ", "")
                elif line.startswith("Name:"):
                    entry["name"] = line.replace("Name: ", "")
                elif line.startswith("Description:"):
                    entry["description"] = line.replace("Description: ", "")
                elif line == "":
                    # End of an entry
                    if entry:
                        cleaned_data.append(entry)
                        entry = {}
        return cleaned_data

    def get_openai_embedding(self, text):
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

    def _save_embeddings_to_json(self):
        # Save the data with embeddings to a JSON file
        with open(self.output_file, 'w') as json_file:
            json.dump(self.embeddings_data, json_file, indent=4)
        print(f"Embeddings data saved to {self.output_file}")

# Run the GenerateEmbeddings class
GenerateEmbeddings()
