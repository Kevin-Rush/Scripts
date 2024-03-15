import ppxt_processor
import convert_slides_to_pdf_to_image
import ppxt_visual_eval
import ppxt_written_eval
import grammar_eval
from extract_script import extract_script
import glob
from colorama import Fore, Style
import pandas as pd
import os

with open("C:/Users/kevin/Documents/Coding/Scripts/gpt_api_key.txt", "r") as file:
    gpt_api_key = file.read()

with open("C:/Users/kevin/Documents/Coding/Scripts/sapling_api_key.txt", "r") as file:
    sapling_api_key = file.read()

with open("C:/Users/kevin/Documents/Coding/Scripts/PowerPoint/course_evaluation/common_generated_terms.txt", "r") as file:
    common_generated_terms = file.read().splitlines()
    print(common_generated_terms)


ppxt_file_glob = glob.glob(r'C:\Users\kevin\Downloads\Week 11 - GAI.pptx')

output_file = "extracted_script.txt"
root = "C:/Users/kevin/Documents/Coding/Scripts/PowerPoint/course_evaluation/"

print(f"{Fore.RESET}Start")
#grammar_eval.evaluate(ppxt_file_glob[0], sapling_api_key)
#print(f"{Fore.GREEN}---------------------Grammar Eval---------------------{Fore.RESET}")
df = ppxt_processor.process(ppxt_file_glob[0])
print(f"{Fore.GREEN}---------------------Slide Deck Contents Saved in DataFrame---------------------{Fore.RESET}")

df = ppxt_written_eval.count_overused_words(df, common_generated_terms)
print(df)
#sum entire columns in the df   
for word in common_generated_terms:
    print(f"{word}: {df[word].sum()}")

df.to_csv(root + "ppxt_pre_eval.csv", index=False)
print(f"{Fore.GREEN}---------------------Common Generated Terms Counted---------------------{Fore.RESET}")
print(f"{Fore.GREEN}---------------------Output Saved---------------------{Fore.RESET}")

#df = pd.read_csv(root + "ppxt_pre_eval.csv")

print(f"{Fore.YELLOW}---------------------Converter Deck to Images---------------------{Fore.RESET}")
convert_slides_to_pdf_to_image.run(ppxt_file_glob, root)
print(f"{Fore.GREEN}---------------------Conversion Successful---------------------{Fore.RESET}")

print(f"{Fore.YELLOW}---------------------Evaluate the Deck---------------------{Fore.RESET}")
df = ppxt_written_eval.evaluate(df, gpt_api_key)
print(f"{Fore.GREEN}---------------------Evaluation Successful---------------------{Fore.RESET}")

#run through all the images in the folder ppxt_images and delete them
print(f"{Fore.YELLOW}---------------------Remove Images---------------------{Fore.RESET}")
dir_path = "ppxt_images/"
img_files = glob.glob(os.path.join(dir_path, "*"))
for img_file in img_files:
    os.remove(img_file)

print(f"{Fore.GREEN}---------------------Images Removed---------------------{Fore.RESET}")

#add two columns to the dataframe, Action Taken (Y/N) and Developer Notes
df['Action Taken to be Taken'] = ""
df['QC Developer Notes'] = ""
df['Content Developer Notes'] = ""

#save the dataframe to a csv
df.to_csv(root + "ppxt_eval.csv", index=False)
print(f"{Fore.GREEN}---------------------Output Saved---------------------{Fore.RESET}")
