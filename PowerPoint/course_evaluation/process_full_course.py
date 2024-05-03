import os

from colorama import Fore
from comment_removal import extract_comments_from_pptx
from ppxt_processor import process
import utils
import pandas as pd
from grammar_eval import check_font_type

def process_ppxt_folder(repository_path, output_file):
    
    # Get all ppxt files in the repository
    
    with open(output_file, "w", encoding='utf-8') as f:

        for ppxt_file in ppxt_files:
            ppxt_file_path = os.path.join(repository_path, ppxt_file)
            output = process(ppxt_file_path)
            
            #iterate through the output df
            for index, row in output.iterrows():
                f.write(f"File: {ppxt_file}\n") 
                f.write(f"Slide Number: {row['Slide Number']}\n")
                f.write(f"Title: {row['Title']}\n")
                f.write(f"Subtitle: {row['Subtitle']}\n")
                f.write(f"Slide Text: {row['Slide Text']}\n")
                f.write(f"Notes Text: {row['Notes Text']}\n")
                f.write("\n")

    print(f"All ppxt files processed. Output saved to {output_file}.")

output_file = "final_output_igai.txt"
repository_path = "C:/Users/kevin/Downloads/IGAI Font Check Test"

ppxt_files = [file for file in os.listdir(repository_path) if file.endswith(".pptx")]
# print(ppxt_files)
i = 1
for pptx_file in ppxt_files:
    # print(f"Checking Font for Week {i} of {len(ppxt_files)}")
    pptx_file_path = os.path.join(repository_path, pptx_file)
    # check_font_type(pptx_file_path)
    print(f"Removing Comments for Week {i} of {len(ppxt_files)}")
    #isolate the file name from pptx_file
    week_name = pptx_file.split(".")[0]
    extract_comments_from_pptx(pptx_file_path, week_name + output_file)


# Call the function to extract comments and remove them from the PowerPoint file


# process_ppxt_folder(ppxt_files)
