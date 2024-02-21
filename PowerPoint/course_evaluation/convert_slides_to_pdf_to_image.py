import os
import glob
from colorama import Fore
import win32com.client
from wand.image import Image
from PIL import Image as PilImage
import numpy as np

def ppxt_to_pdf(files, root, formatType = 32):
    # Convert ppxt to PDF using win32com
    powerpoint = win32com.client.Dispatch("Powerpoint.Application")
    powerpoint.Visible = 1

    for filename in files:
        print("Filename: ", filename)
        newname = os.path.splitext(filename)[0] + ".pdf"
        print("Newname: ", newname)
        deck = powerpoint.Presentations.Open(filename)
        deck.SaveAs(newname, formatType)
        deck.Close()
    powerpoint.Quit()

    print("File converted to PDF")


def pdf_to_images(pdf_file, output_folder):
    # Convert PDF to images using wand
    with Image(filename=pdf_file, resolution=300) as img:
        img.compression_quality = 99
        # Iterate over each page in the PDF
        for i, page in enumerate(img.sequence):
            percentage = int((i / len(img.sequence)) * 100)
            loading_bar = '#' * (percentage // 2 + 2) + '-' * (50 - percentage // 2)
            print(f" Processing page: {i+1} of {len(img.sequence)} \r[{loading_bar}] {percentage}%", end='')

            # Convert wand image to PIL image
            pil_img = PilImage.fromarray(np.array(page))
            # Convert image to RGB mode
            rgb_img = pil_img.convert("RGB")
            # Resize the image
            max_size = (518, 518)
            rgb_img.thumbnail(max_size, PilImage.ANTIALIAS)
            # Save the image with a unique filename
            base_filename = "slide"
            extension = ".jpg"
            if i < 9:
                rgb_img.save(output_folder + base_filename + "_0" + str(i+1) + extension, "JPEG")
            else:
                rgb_img.save(output_folder + base_filename + "_" + str(i+1) + extension, "JPEG")
        
    print()


def run(ppxt_file, root):
    # Convert ppxt to PDF to images
    print(f"{Fore.YELLOW}---------------------Convert to PDF---------------------{Fore.RESET}")
    ppxt_to_pdf(ppxt_file, root)
    print(f"{Fore.YELLOW}---------------------Save Images---------------------{Fore.RESET}")

    #Note to self, need to make the folder creation and tracking more robust. Right now this is dependent on the folder existing and the script being run from within the PowerPoint parent folder

    pdf_file = r"C:\Users\kevin\Downloads\Slides Week 9 - GAI.pdf"
    output_folder = root + "ppxt_images/"
    pdf_to_images(pdf_file, output_folder)
