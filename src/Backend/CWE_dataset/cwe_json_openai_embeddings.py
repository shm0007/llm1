import openai
import json
import xml.etree.ElementTree as ET
import os
from dotenv import load_dotenv

# Load environment variables from a .env file (for API keys)
load_dotenv()

# Set your OpenAI API key from environment variable
openai.api_key = os.getenv('OPENAI_API_KEY')

# Step 1: Parse XML file and extract CWE data
namespace = {'cwe': 'http://cwe.mitre.org/cwe-7'}
file_name = '/Users/consueloramirez/Desktop/Attack/cwe-attack-chat-tool/datasets/CWE/1000.xml'  # Replace with your actual XML file path

# Function to parse a single CWE entry from XML
def parse_weakness_as_string(weakness_element):
    description_elem = weakness_element.find('cwe:Description', namespace)
    description = description_elem.text.strip() if description_elem is not None and description_elem.text else ''
    
    extended_description_elem = weakness_element.find('cwe:Extended_Description', namespace)
    extended_description = ''.join(extended_description_elem.itertext()).strip() if extended_description_elem is not None else ''
    
    cwe_entry = {
        "ID": weakness_element.get('ID'),
        "Name": weakness_element.get('Name'),
        "Description": description,
        "Extended_Description": extended_description
    }
    return cwe_entry

# Load and parse XML
tree = ET.parse(file_name)
root = tree.getroot()
cwe_data = [parse_weakness_as_string(weak_elem) for weak_elem in root.findall('.//cwe:Weakness', namespace)]

# Step 2: Define a function to generate embeddings with OpenAI
def get_openai_embedding(text):
    try:
        # Use OpenAI's new embedding API (using the 'embeddings' endpoint)
        response = openai.embeddings.create(
            model="text-embedding-ada-002",  # Ensure to use the correct model name
            input=text
        )
        # Access the embedding from the response using the .data attribute
        embedding = response.data[0].embedding
        return embedding
    except Exception as e:
        print(f"Error generating embedding: {e}")
        return None

# Step 3: Vectorize the CWE entries using OpenAI embeddings
embedding_data = []
for entry in cwe_data:
    # Combine text fields to create a comprehensive input for embedding
    text_to_vectorize = f"{entry['Name']} {entry['Description']} {entry['Extended_Description']}"
    embedding = get_openai_embedding(text_to_vectorize)  # Generate embedding
    if embedding:
        entry_with_embedding = {
            "cweID": entry['ID'],
            "name": entry['Name'],
            "description": entry['Description'],
            "extendedDescription": entry['Extended_Description'],
            "embedding": embedding
        }
        embedding_data.append(entry_with_embedding)  # Append the entry with embedding to the list

# Step 4: Save embeddings and data to a JSON file
output_file = '/Users/consueloramirez/Desktop/Attack/cwe-attack-chat-tool/src/Backend/CWE_dataset/openapi_cwe_embeddings.json'  # Replace with your desired output path
with open(output_file, 'w') as f:
    json.dump(embedding_data, f, indent=4)  # Save as JSON with indentation for readability

print(f"Embeddings saved to {output_file}")

