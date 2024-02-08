import os
import base64
import requests
import openai

# Function to encode the image
def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def run(output_folder, api_key):
    openai.api_key = api_key
    # Get a list of the image files
    image_files = os.listdir(output_folder)

    # Iterate over the image files
    for image_file in image_files:
        # Full path to the image file
        image_path = os.path.join(output_folder, image_file)
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
                "text": "You are a powerpoint slide evaluator. Your job is to review the slide and provide feedback on the clarity, simplicity, and visual appeal of the slide. For clarity and simplicity I want you to tell me if the information being presented is given in a direct and pithy way that does not use any extravegant phrasing. For visual appeal, I want you to tell me if the information on the slide is presented in an effective way. Ensure that you say 1 good thing about the slide, but then provide specific and actionable feedback. Please only consider the text I've given, do not think beyond the slide."
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