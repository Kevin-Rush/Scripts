
import ppxt_processor
import convert_slides_to_pdf_to_image
import ppxt_visual_eval
import subprocess
import glob
import openai


with open("C:/Users/kevin/Documents/Coding/Scripts/gpt_api_key.txt", "r") as file:
    api_key = file.read()

ppxt_file = glob.glob(r'C:\Users\kevin\Documents\Coding\Scripts\PowerPoint\test_file.pptx')

root = "C:/Users/kevin/Documents/Coding/Scripts/PowerPoint/"

df = ppxt_processor.process_ppxt(ppxt_file[0])
print(df)
#convert_slides_to_pdf_to_image.run(ppxt_file, root)
#ppxt_visual_eval.run()