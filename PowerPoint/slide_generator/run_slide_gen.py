import os
import script_converter
import slide_deck_generator
import slide_image_gen

# Input file
file_name = "impact_festival_extension"

input_file = "scripts/"+file_name+".txt"
json_script = "scripts/"+file_name+".json"
base_ppxt = 'base_presentation.pptx'

#read my api key from the gpt_key.txt file
with open(r"C:\Users\kevin\Documents\Coding\Scripts\gpt_api_key.txt", "r") as file:
    api_key = file.read()

#Or hard code the api key
#api_key = ""  

script_converter.convert_to_json(input_file, json_script, api_key)
slide_deck_generator.generate_presentation(json_script, base_ppxt)

#change the file named generated_presentation.pptx to file_name.pptx
os.rename("generated_presentation.pptx", file_name+".pptx")

generated_presentation = file_name+".pptx"
slide_image_gen.gen_image_for_slide(json_script, generated_presentation, api_key)

#open the generated presentation
os.system(generated_presentation)
