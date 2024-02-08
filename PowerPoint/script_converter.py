import json

def convert_to_json(input_file, output_file):
    with open(input_file, 'r') as file:
        paragraphs = file.read().split('\n\n')  # Split text into paragraphs

    data = []
    for paragraph in paragraphs:
        data.append({'paragraph': paragraph.strip()})  # Create a dictionary entry for each paragraph

    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)  # Write data to JSON file

# Usage example
input_file = '/path/to/raw_text.txt'
output_file = '/path/to/output.json'
convert_to_json(input_file, output_file)
