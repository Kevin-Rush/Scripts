import os
import script_converter
import slide_deck_generator
import slide_image_gen

# Input file
input_file = "" #enter the path to the input txt script file 
json_script = "scripts/automation_presentation_script.json" #enter the path to the output json script file
base_ppxt = '' #enter the name of the base powerpoint file that will use the master slide as the template for the generated presentation

#read my api key from the gpt_key.txt file
with open(r"", "r") as file:
    api_key = file.read()

#Or hard code the api key
#api_key = ""  

script_converter.convert_to_json(input_file, json_script, api_key)
slide_deck_generator.generate_presentation(json_script, base_ppxt)

generated_presentation = "generated_presentation.pptx"
slide_image_gen.gen_image_for_slide(json_script, generated_presentation, api_key)

#open the generated presentation
os.system(generated_presentation)
