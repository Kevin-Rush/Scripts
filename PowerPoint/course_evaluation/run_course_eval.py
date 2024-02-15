import ppxt_processor
import convert_slides_to_pdf_to_image
import ppxt_visual_eval
import ppxt_written_eval
from extract_script import extract_script
import glob
from colorama import Fore, Style

with open("C:/Users/kevin/Documents/Coding/Scripts/gpt_api_key.txt", "r") as file:
    api_key = file.read()

ppxt_file_glob = glob.glob(r'C:\Users\kevin\Downloads\Slides_Week_5_GAI.pptx')
# print("ppxt_file_glob: ", ppxt_file_glob)
# print("ppxt_file_glob[0]: ", ppxt_file_glob[0])

#ppxt_file = "Slides_Week_5_GAI.pptx"
output_file = "extracted_script.txt"
root = "C:/Users/kevin/Documents/Coding/Scripts/PowerPoint/course_evaluation/"

print(f"{Fore.RESET}Start")
df = ppxt_processor.process(ppxt_file_glob[0])
print(f"{Fore.GREEN}---------------------Slide Deck Contents Saved in DataFrame---------------------{Fore.RESET}")

#print all the columns of the dataframe
print(df.head(1))

print(f"{Fore.YELLOW}---------------------Converter Deck to Images---------------------")
#convert_slides_to_pdf_to_image.run(ppxt_file_glob, root)
print(f"{Fore.GREEN}---------------------Conversion Successful---------------------{Fore.RESET}")

print(f"{Fore.YELLOW}---------------------Evaluate the Deck---------------------{Fore.RESET}")
#df = ppxt_written_eval.evaluate(df, api_key)
print(f"{Fore.GREEN}---------------------Conversion Successful---------------------{Fore.RESET}")

#use chatgpt to do a visual evaluation of all the slides
#responses = ppxt_visual_eval.run(root + "ppxt_images/", api_key)

# #run through the list responses and add them to the dataframe
# for i, response in enumerate(responses):
#     df.at[i, 'Response'] = response

#save the dataframe to a csv
df.to_csv(root + "ppxt_eval.csv", index=False)
print(f"{Fore.GREEN}---------------------Output Saved---------------------{Fore.RESET}")