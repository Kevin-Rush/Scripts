import sys
import os
import glob
import win32com.client
from pdf2image import convert_from_path
from wand.image import Image
import openai
import base64
import requests
from PIL import Image as PilImage
import numpy as np
import random

with open("C:/Users/kevin/Documents/Coding/Scripts/gpt_api_key.txt", "r") as file:
    api_key = file.read()

openai.api_key = api_key

def convert(files, formatType = 32):
    powerpoint = win32com.client.Dispatch("Powerpoint.Application")
    powerpoint.Visible = 1
    for filename in files:
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
            rgb_img.save(output_folder + base_filename + "_" + str(i) + extension, "JPEG")

files = glob.glob(r'C:\Users\kevin\Documents\Coding\Scripts\PowerPoint\test_file.pptx')
convert(files)

root = "C:/Users/kevin/Documents/Coding/Scripts/PowerPoint/"
pdf_file = root + "/test_file.pdf"
output_folder = root + "ppxt_images/"
pdf_to_images(pdf_file, output_folder)