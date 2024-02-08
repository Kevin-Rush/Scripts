
import ppxt_evaluator
import convert_slides_to_pdf_to_image
import ppxt_visual_eval
import subprocess
import glob
import openai


with open("C:/Users/kevin/Documents/Coding/Scripts/gpt_api_key.txt", "r") as file:
    api_key = file.read()

ppxt_files = glob.glob(r'C:\Users\kevin\Documents\Coding\Scripts\PowerPoint\test_file.pptx')

root = "C:/Users/kevin/Documents/Coding/Scripts/PowerPoint/"

convert_slides_to_pdf_to_image.run(ppxt_files, root)
ppxt_visual_eval.run()