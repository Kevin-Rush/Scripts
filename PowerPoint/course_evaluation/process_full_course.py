import os
import csv
import sys

def process_ppxt_files(repository_path):
    output_file = "output.txt"
    ppxt_processor = "ppxt_processor.py"
    ppxt_files = [file for file in os.listdir(repository_path) if file.endswith(".ppxt")]

    with open(output_file, "w", newline="") as f:
        sys.stdout = f

        for ppxt_file in ppxt_files:
            ppxt_file_path = os.path.join(repository_path, ppxt_file)
            output = os.popen(f"python {ppxt_processor} {ppxt_file_path}").read().strip()


    print(f"All ppxt files processed. Output saved to {output_file}.")
