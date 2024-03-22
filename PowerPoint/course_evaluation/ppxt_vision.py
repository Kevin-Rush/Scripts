import os
import base64
from colorama import Fore
import requests
import openai

with open("C:/Users/kevin/Documents/Coding/Scripts/gpt_api_key.txt", "r") as file:
    gpt_api_key = file.read()

# Function to encode the image
def encode_image(image_path):
    #This function encodes the image to base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def generate_alt_text(image):
    # This function takes an image and returns the alt text for the image
    prompt = "You are a powerpoint slide evaluator. Your job is to review the slide and provide feedback on the clarity, simplicity, and visual appeal of the slide. For clarity and simplicity I want you to tell me if the information being presented is given in a direct and pithy way that does not use any extravegant phrasing (extravegant phrasing includes but is not restricted to: 'delve', 'utilize', 'the art and science of', 'enter the world of', etc.). For visual appeal, I want you to tell me if the information on the slide is presented effectively. Do not say ANYTHING about colour pallet or font size becaues these are standardized by our client and cannot be changed. Therefore, only give actionable feedback. Ensure that you say 1 good thing about the slide, and then provide 3 specific and actionable pieces feedback. Keep responses short and direct yet professional and only consider the text I've given, do not think beyond the slide. Also, in the spirit of brievity, if a slide is good feel free to simply state, this slide is good IF there is no actionable feedback to give. Slide:"

    base64_image = encode_image(image)
    response = call_gpt_vision(base64_image, prompt)
    print(f"{Fore.GREEN}\n-----------------Image Processed-----------------{Fore.RESET}")

    return response


def slide_eval(image_path):
    # This function takes a folder of images and an API key and returns a list of responses from the GPT-4 Vision model
    print(image_path)
    prompt = "You are a powerpoint slide evaluator. Your job is to review the slide and provide feedback on the clarity, simplicity, and visual appeal of the slide. For clarity and simplicity I want you to tell me if the information being presented is given in a direct and pithy way that does not use any extravegant phrasing (extravegant phrasing includes but is not restricted to: 'delve', 'utilize', 'the art and science of', 'enter the world of', etc.). For visual appeal, I want you to tell me if the information on the slide is presented effectively. Do not say ANYTHING about colour pallet or font size becaues these are standardized by our client and cannot be changed. Therefore, only give actionable feedback. Ensure that you say 1 good thing about the slide, and then provide 3 specific and actionable pieces feedback. Keep responses short and direct yet professional and only consider the text I've given, do not think beyond the slide. Also, in the spirit of brievity, if a slide is good feel free to simply state, this slide is good IF there is no actionable feedback to give. Slide:"

    base64_image = encode_image(image_path)
    response = call_gpt_vision(base64_image, prompt)
    print(f"{Fore.GREEN}\n-----------------Image Processed-----------------{Fore.RESET}")

    return response

def read_SM_slide(image_path, additional_text):
    prompt = "You are a powerpoint slide describer. Your job is to take in an image of a slide that contains graphics and describe the slide as accurately as possible for the visually impaired. You need to identify the text within the slide and describe how the visual effects on the slide are used to alongside the text. Your response should professional and easy to follow. The slides also have a notes section: " + additional_text + "Use these notes to help inform you about what this slide is about."

    base64_image = encode_image(image_path)
    response = call_gpt_vision(base64_image, prompt)
    print(f"{Fore.GREEN}---------------------Smart Art Read---------------------{Fore.RESET}")

    return response['choices'][0]['message']['content']

def call_gpt_vision(base64_image, prompt):
    # This function takes a folder of images and an API key and returns a list of responses from the GPT-4 Vision model
    openai.api_key = gpt_api_key
    model = "gpt-4-vision-preview"

    headers = {
    "Content-Type": "application/json",
    "Authorization": f"Bearer {gpt_api_key}"
    }

    payload = {
    "model": model,
    "messages": [
        {
        "role": "user",
        "content": [
            {
            "type": "text",
            "text": prompt
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

    return response