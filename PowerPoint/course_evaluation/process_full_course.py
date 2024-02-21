import os
from ppxt_processor import process

def process_ppxt_files(repository_path):
    output_file = "output.txt"
    ppxt_processor = "ppxt_processor.py"
    # Get all ppxt files in the repository
    ppxt_files = [file for file in os.listdir(repository_path) if file.endswith(".pptx")]
    print(ppxt_files)
    
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

repository_path = "C:/Users/kevin/Downloads/course"

process_ppxt_files(repository_path)
