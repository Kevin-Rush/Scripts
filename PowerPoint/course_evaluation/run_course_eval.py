import ppxt_processor
import convert_slides_to_pdf_to_image
import ppxt_visual_eval
import ppxt_written_eval
from extract_script import extract_script
import glob
from colorama import Fore, Style
import os

with open("", "r") as file: #enter the path to the gpt_key.txt file
    api_key = file.read()

#or hard code the api key
#api_key = ""  

ppxt_file_glob = glob.glob(r'') #enter the path to the ppxt file

output_file = "extracted_script.txt"
root = "" #enter the path to the root folder

print(f"{Fore.RESET}Start")
df = ppxt_processor.process(ppxt_file_glob[0])
print(f"{Fore.GREEN}---------------------Slide Deck Contents Saved in DataFrame---------------------{Fore.RESET}")

#print all the columns of the dataframe
print(df.head(1))

print(f"{Fore.YELLOW}---------------------Converter Deck to Images---------------------{Fore.RESET}")
convert_slides_to_pdf_to_image.run(ppxt_file_glob, root)
print(f"{Fore.GREEN}---------------------Conversion Successful---------------------{Fore.RESET}")

print(f"{Fore.YELLOW}---------------------Evaluate the Deck---------------------{Fore.RESET}")
df = ppxt_written_eval.evaluate(df, api_key)
print(f"{Fore.GREEN}---------------------Evaluation Successful---------------------{Fore.RESET}")

#run through all the images in the folder ppxt_images and delete them
print(f"{Fore.YELLOW}---------------------Remove Images---------------------{Fore.RESET}")

dir_path = "ppxt_images/"
img_files = glob.glob(os.path.join(dir_path, "*"))
for img_file in img_files:
    os.remove(img_file)

print(f"{Fore.GREEN}---------------------Images Removed---------------------{Fore.RESET}")

#add new columns to the dataframe
df['Response'] = ""
df['Visual Evaluation'] = ""


#save the dataframe to a csv
df.to_csv(root + "ppxt_eval.csv", index=False)
print(f"{Fore.GREEN}---------------------Output Saved---------------------{Fore.RESET}")