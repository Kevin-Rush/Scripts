import ppxt_processor
import convert_slides_to_pdf_to_image
import ppxt_visual_eval
from extract_script import extract_script
import glob

with open("C:/Users/kevin/Documents/Coding/Scripts/gpt_api_key.txt", "r") as file:
    api_key = file.read()

ppxt_file_glob = glob.glob(r'C:\Users\kevin\Documents\Coding\Scripts\PowerPoint\course_evaluation\test_file.pptx')
# print("ppxt_file_glob: ", ppxt_file_glob)
# print("ppxt_file_glob[0]: ", ppxt_file_glob[0])

ppxt_file = "[Slides] Week 5 - GAI.pptx"
output_file = "extracted_script.txt"
root = "C:/Users/kevin/Documents/Coding/Scripts/PowerPoint/course_evaluation/"

df = ppxt_processor.process(ppxt_file)

# for i in range(len(df)):
#     print("Slide Number: " + str(df["Slide Number"][i]) + " Type: " + df["Slide Type"][i])

#print("---------------------Call Converter---------------------")
#convert_slides_to_pdf_to_image.run(ppxt_file_glob, root)
#responses = ppxt_visual_eval.run(root + "ppxt_images/", api_key)

# #run through the list responses and add them to the dataframe
# for i, response in enumerate(responses):
#     df.at[i, 'Response'] = response

# #save the dataframe to a csv
# df.to_csv(root + "ppxt_eval.csv", index=False)