import ppxt_processor
import convert_slides_to_pdf_to_image
import ppxt_text as ppxt_text
import grammar_eval
from extract_script import extract_script
import glob
from colorama import Fore, Style
import pandas as pd
import os

with open("C:/Users/kevin/Documents/Coding/Scripts/sapling_api_key.txt", "r") as file:
    sapling_api_key = file.read()

with open("C:/Users/kevin/Documents/Coding/Scripts/PowerPoint/course_evaluation/common_generated_terms.txt", "r") as file:
    common_generated_terms = file.read().splitlines()

root = "C:/Users/kevin/Documents/Coding/Scripts/PowerPoint/course_evaluation/"

def run_eval(ppxt_file_glob, file_name):
    print(f"{Fore.RESET}Start")

    print(f"{Fore.YELLOW}---------------------Create Slide Images---------------------{Fore.RESET}")
    convert_slides_to_pdf_to_image.run(ppxt_file_glob, root)
    print(f"{Fore.GREEN}---------------------Image Creation Successful---------------------{Fore.RESET}")

    # grammar_eval.evaluate(ppxt_file_glob[0], sapling_api_key)
    # print(f"{Fore.GREEN}---------------------Grammar Eval---------------------{Fore.RESET}")
    print(ppxt_file_glob)
    print(ppxt_file_glob[0])
    
    df = ppxt_processor.process(ppxt_file_glob[0])
    print(f"{Fore.GREEN}---------------------Slide Deck Contents Saved in DataFrame---------------------{Fore.RESET}")

    df = ppxt_text.count_overused_words(df, common_generated_terms)
    print(df)
    #sum entire columns in the df   
    for word in common_generated_terms:
        print(f"{word}: {df[word].sum()}")
    print(f"{Fore.GREEN}---------------------Common Generated Terms Counted---------------------{Fore.RESET}")

    df.to_csv(root + file_name + "ppxt_pre_eval.csv", index=False)
    print(f"{Fore.GREEN}---------------------Output Saved---------------------{Fore.RESET}")

    # df = pd.read_csv(root + file_name + "ppxt_pre_eval.csv")

    print(f"{Fore.YELLOW}---------------------Evaluate the Deck---------------------{Fore.RESET}")

    #track doc in the token_logs.txt file
    with open("token_logs.txt", "a") as f:
        f.write(ppxt_file_glob[0])

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
    df.to_csv(root + file_name + "ppxt_eval.csv", index=False)
    print(f"{Fore.GREEN}---------------------Output Saved---------------------{Fore.RESET}")



single_ppxt = False
user_verification = input("Have you updated the single_ppxt and file path? (Y/N) ")

if user_verification == "N" or user_verification == "n":
    print("Please update the single_ppxt variable and file path in the script and run again.")
    exit()

if single_ppxt:
    ppxt_file_glob = glob.glob(r'C:\Users\kevin\Downloads\Module 6.pptx')
    file_name = ppxt_file_glob[0].split("\\")[-1]
    run_eval(ppxt_file_glob, file_name)
else:
    #run through an entire folder of ppxt files
    ppxt_file_glob = glob.glob(r'C:\Users\kevin\Downloads\M4AI\*.pptx')
    k = 0
    for i in ppxt_file_glob:
        file_name = ppxt_file_glob[k].split("\\")[-1]
        run_eval([i], file_name)
        k += 1
    