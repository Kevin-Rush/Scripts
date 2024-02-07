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

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

files = glob.glob(r'C:\Users\kevin\Documents\Coding\Scripts\PowerPoint\test_file.pptx')
convert(files)

root = "C:/Users/kevin/Documents/Coding/Scripts/PowerPoint/"
pdf_file = root + "/test_file.pdf"
output_folder = root + "ppxt_images/"
pdf_to_images(pdf_file, output_folder)


# Get a list of the image files
image_files = os.listdir(output_folder)

# Full path to the image file
image_path = r"C:\Users\kevin\Documents\Coding\Scripts\PowerPoint\ppxt_images\slide_5.jpg"
base64_image = encode_image(image_path)

headers = {
"Content-Type": "application/json",
"Authorization": f"Bearer {api_key}"
}

payload = {
"model": "gpt-4-vision-preview",
"messages": [
    {
    "role": "user",
    "content": [
        {
        "type": "text",
        "text": "You are a powerpoint slide evaluator. Your job is to review the slide and provide feedback on the clarity, simplicity, and visual appeal of the slide. For clarity and simplicity I want you to tell me if the information being presented is given in a direct and pithy way that does not use any extravegant phrasing. For visual appeal, I want you to tell me if the information on the slide is presented in an effective way. Ensure to provide specific and actionable feedback. You should also provide feedback on the overall quality of the slide. Please only consider the text I've given."
        },
        {
        "type": "image_url",
        "image_url": {
            "url": f"data:image/jpeg;base64,{base64_image}"
        }
        }
    ]
    }
],
"max_tokens": 1251
}

response = requests.post("https://api.openai.com/v1/chat/completions", headers=headers, json=payload)
response = response.json()

tokens = response['usage']
response = response['choices'][0]['message']['content']
print(response)
print("Tokesn used: ", tokens)