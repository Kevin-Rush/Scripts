import os

from colorama import Fore
from ppxt_processor import process
import utils
import pandas as pd

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

output_file = "output.txt"
repository_path = "C:/Users/kevin/Downloads/IGAI Course"

ppxt_files = [file for file in os.listdir(repository_path) if file.endswith(".pptx")]
# print(ppxt_files)

process_ppxt_folder(ppxt_files)
