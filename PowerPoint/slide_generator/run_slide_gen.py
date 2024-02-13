
import script_converter
import slide_deck_generator

# Input file
input_file = "test_script.txt"
json_script = "script.json"
base_ppxt = 'base_presentation.pptx'

#read my api key from the gpt_key.txt file
with open("gpt_key.txt", "r") as file:
    api_key = file.read()

#Or hard code the api key
#api_key = ""  

script_converter.convert_to_json(input_file, json_script, api_key)
slide_deck_generator.generate_presentation(json_script, base_ppxt)
