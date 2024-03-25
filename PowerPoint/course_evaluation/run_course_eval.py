import ppxt_processor
import convert_slides_to_pdf_to_image
import ppxt_text as ppxt_text
import grammar_eval
from extract_script import extract_script
import glob
from colorama import Fore, Style
import pandas as pd
import os

ppxt_file_glob = glob.glob(r'ENTER_PPXT_FILE_PATH_HERE')

output_file = "extracted_script.txt"
root = "ENTER_THE_ROOT_PATH_HERE"

with open("C:/Users/kevin/Documents/Coding/Scripts/PowerPoint/course_evaluation/common_generated_terms.txt", "r") as file:
    common_generated_terms = file.read().splitlines()

print(f"{Fore.RESET}Start")

print(f"{Fore.YELLOW}---------------------Create Slide Images---------------------{Fore.RESET}")
convert_slides_to_pdf_to_image.run(ppxt_file_glob, root)
print(f"{Fore.GREEN}---------------------Image Creation Successful---------------------{Fore.RESET}")

#print(f"{Fore.GREEN}---------------------Grammar Eval---------------------{Fore.RESET}")
df = ppxt_processor.process(ppxt_file_glob[0])
print(f"{Fore.GREEN}---------------------Slide Deck Contents Saved in DataFrame---------------------{Fore.RESET}")

df = ppxt_text.count_overused_words(df, common_generated_terms)
print(df)
#sum entire columns in the df   
for word in common_generated_terms:
    print(f"{word}: {df[word].sum()}")
print(f"{Fore.GREEN}---------------------Common Generated Terms Counted---------------------{Fore.RESET}")

df.to_csv(root + "ppxt_pre_eval.csv", index=False)
print(f"{Fore.GREEN}---------------------Output Saved---------------------{Fore.RESET}")

# df = pd.read_csv(root + "ppxt_pre_eval.csv")

print(f"{Fore.YELLOW}---------------------Evaluate the Deck---------------------{Fore.RESET}")
df = ppxt_text.evaluate_slide_df(df)
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
