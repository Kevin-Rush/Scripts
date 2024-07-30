

"""
This script processes a folder containing PowerPoint files (.pptx) and extracts information from each slide, such as slide number, title, subtitle, slide text, and notes text. It then saves the extracted information to a text file.

The script first imports necessary modules and functions, including 'os' for file operations, 'colorama' for colored output, 'comment_removal' for extracting comments from PowerPoint files, 'ppxt_processor' for processing the PowerPoint files, 'utils' for utility functions, 'pandas' for data manipulation, and 'grammar_eval' for checking font types.

The main function 'process_ppxt_folder' takes the repository path and output file path as input. It iterates through all the PowerPoint files in the repository, processes each file using the 'process' function, and writes the extracted information to the output file. The information includes the file name, slide number, title, subtitle, slide text, and notes text.

After processing all the PowerPoint files, the script prints a message indicating that all files have been processed and the output file has been saved.

The script also defines a list of PowerPoint files 'ppxt_files' by recursively searching for files with the '.pptx' extension in the repository path. It then iterates through each PowerPoint file, checks the font type using the 'check_font_type' function, and removes comments from the PowerPoint file using the 'extract_comments_from_pptx' function.

To use this script, provide the repository path and output file path as arguments to the 'process_ppxt_folder' function and run the script.
"""

import os
from colorama import Fore
from comment_removal import extract_comments_from_pptx
from ppxt_processor import process
import utils
import pandas as pd
from grammar_eval import check_font_type

# Rest of the code...
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

output_file = "final_comments_igai.txt"
repository_path = "C:/Users/kevin/Downloads/OneDrive_2024-05-03"

ppxt_files = [os.path.join(root, file) 
              for root, dirs, files in os.walk(repository_path) 
              for file in files if file.endswith(".pptx")]
# for ppxt_file in ppxt_files:
#     print(ppxt_file)
i = 1
for pptx_file in ppxt_files:
    # print(f"Checking Font for Week {i} of {len(ppxt_files)}")
    pptx_file_path = os.path.join(repository_path, pptx_file)
    # check_font_type(pptx_file_path)
    #isolate the file name from pptx_file
    week_name = pptx_file.split(".")[0]
    print(f"Removing Comments for {week_name} of {len(ppxt_files)}")

    extract_comments_from_pptx(pptx_file_path, week_name + output_file)
    i += 1


# Call the function to extract comments and remove them from the PowerPoint file


# process_ppxt_folder(ppxt_files)
