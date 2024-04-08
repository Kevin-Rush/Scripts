#useful functions used across multiple scripts
import json


def print_loader (length, i):
    #print a loading bar for a dataframe
    percentage = int((i / length) * 100)
    loading_bar = '#' * (percentage // 2 + 2) + '-' * (50 - percentage // 2)
    print(f"\r[{loading_bar}] {percentage}%", end='')
    if percentage == 100:
        print()

def clean_filename(filename):
    #clean a filename to remove any special characters
    if "[Slides] " in filename:
        filename = filename.replace("[Slides] ", "")
    if " (1)" in filename:
        filename = filename.replace(" (1)", "")
    return filename

def convert_txt_JSON(filename):
    #convert a txt file to a JSON file
    with open(filename, 'r') as file:
        lines = file.readlines()
        data = {}
        for line in lines:
            line = line.split(":")
            key, value = line.split(":")
            data[key.strip()] = value.strip()

    #write the data to a JSON file
    print(data)
    with open(filename.split(".")[0] + ".json", 'a') as file:
        json.dump(data, file)

   
    
filename = "token_logs.txt"
convert_txt_JSON(filename)