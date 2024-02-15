import os
import script_converter
import slide_deck_generator
import slide_image_gen

# Input file
input_file = "scripts/automation_presentation.txt"
json_script = "scripts/automation_presentation_script.json"
base_ppxt = 'base_presentation.pptx'

#read my api key from the gpt_key.txt file
with open(r"C:\Users\kevin\Documents\Coding\Scripts\gpt_api_key.txt", "r") as file:
    api_key = file.read()

#Or hard code the api key
#api_key = ""  

script_converter.convert_to_json(input_file, json_script, api_key)
slide_deck_generator.generate_presentation(json_script, base_ppxt)

generated_presentation = "generated_presentation.pptx"
slide_image_gen.gen_image_for_slide(json_script, generated_presentation, api_key)

#open the generated presentation
os.system(generated_presentation)
