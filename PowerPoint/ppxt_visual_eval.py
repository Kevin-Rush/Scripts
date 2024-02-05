import sys
import os
import glob
import win32com.client
from pdf2image import convert_from_path
from wand.image import Image


def convert(files, formatType = 32):
    powerpoint = win32com.client.Dispatch("Powerpoint.Application")
    powerpoint.Visible = 1
    for filename in files:
        newname = os.path.splitext(filename)[0] + ".pdf"
        deck = powerpoint.Presentations.Open(filename)
        deck.SaveAs(newname, formatType)
        deck.Close()
    powerpoint.Quit()

def pdf_to_images(pdf_file):
    # Convert PDF to images using wand
    with Image(filename=pdf_file, resolution=300) as img:
        img.compression_quality = 99
        img.save(filename="output.jpg")

files = glob.glob(r'C:\Users\kevin\Downloads\test_file.pptx')
convert(files)

pdf_file = "C:/Users/kevin/Downloads/test_file.pdf"
pdf_to_images(pdf_file)