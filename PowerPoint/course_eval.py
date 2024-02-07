
import ppxt_evaluator
import convert_slides_to_pdf_to_image
import ppxt_visual_eval
import subprocess
import glob

# Call a function from the other file
ppxt_evaluator.some_function()

# Call and run the ppxt_evaluator.py file
subprocess.run(['python', '/path/to/ppxt_evaluator.py'])

ppxt_files = glob.glob(r'C:\Users\kevin\Documents\Coding\Scripts\PowerPoint\test_file.pptx')
