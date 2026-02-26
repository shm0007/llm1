import xml.etree.ElementTree as ET

# File name of your XML file
file_name = '1000.xml'  

# Define the XML namespace used in the document
namespace = {'cwe': 'http://cwe.mitre.org/cwe-7'}

# Function to extract desired fields and format as a string
def parse_weakness_as_string(weakness_element):
    # Extract Description
    description_elem = weakness_element.find('cwe:Description', namespace)
    description = description_elem.text.strip() if description_elem is not None and description_elem.text is not None else ''
    
    # Extract Extended_Description
    extended_description_elem = weakness_element.find('cwe:Extended_Description', namespace)
    if extended_description_elem is not None:
        # Extract all text content, including from nested tags
        extended_description = ''.join(extended_description_elem.itertext()).strip()
    else:
        extended_description = ''
    
    # Format the entry as a string
    formatted_string = (
        f"ID: {weakness_element.get('ID')}\n"
        f"Name: {weakness_element.get('Name')}\n"
        f"Description: {description}\n"
        f"Extended Description: {extended_description}\n"
    )
    
    return formatted_string

# List to store parsed weaknesses as formatted strings
formatted_weaknesses = []

# Parse the XML file
tree = ET.parse(file_name)
root = tree.getroot()

# Iterate through each Weakness element
for weakness_elem in root.findall('.//cwe:Weakness', namespace):
    formatted_weaknesses.append(parse_weakness_as_string(weakness_elem))

# Check if any weaknesses were parsed
if len(formatted_weaknesses) == 0:
    print("No weaknesses were parsed. Please check the XML structure.")
else:
    print(f"Total weaknesses parsed: {len(formatted_weaknesses)}")

# Save the formatted data as a text file
output_file_path = 'formatted_cwe_entries.txt'  # Save in the current directory

# Write formatted strings to the file
with open(output_file_path, 'w', encoding='utf-8') as file:
    for formatted_string in formatted_weaknesses:
        file.write(formatted_string + "\n\n")  # Add a newline to separate entries

print(f"Data saved as formatted strings at: {output_file_path}")
