import os
import glob
import win32com.client
from wand.image import Image
from PIL import Image as PilImage
import numpy as np

def ppxt_to_pdf(files, formatType = 32):
    # Convert ppxt to PDF using win32com
    print("files: ", files)
    powerpoint = win32com.client.Dispatch("Powerpoint.Application")
    powerpoint.Visible = 1
    for filename in files:
        print("filename: ", filename)
        newname = os.path.splitext(filename)[0] + ".pdf"
        deck = powerpoint.Presentations.Open(filename)
        deck.SaveAs(newname, formatType)
        deck.Close()
    powerpoint.Quit()


def pdf_to_images(pdf_file, output_folder):
    # Convert PDF to images using wand
    with Image(filename=pdf_file, resolution=300) as img:
        img.compression_quality = 99
        # Iterate over each page in the PDF
        for i, page in enumerate(img.sequence):
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
            if i < 10:
                rgb_img.save(output_folder + base_filename + "_0" + str(i+1) + extension, "JPEG")
            else:
                rgb_img.save(output_folder + base_filename + "_" + str(i+1) + extension, "JPEG")


def run(ppxt_file, root):
    # Convert ppxt to PDF to images
    print("---------------------Convert to PDF---------------------")
    ppxt_to_pdf(ppxt_file)
    print("---------------------Convert to Images---------------------")

    #Note to self, need to make the folder creation and tracking more robust. Right now this is dependent on the folder existing and the script being run from within the PowerPoint parent folder

    pdf_file = root + "test_file.pdf"

    output_folder = root + "ppxt_images/"

    pdf_to_images(pdf_file, output_folder)