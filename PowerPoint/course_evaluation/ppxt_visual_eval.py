import os
import base64
import requests
import openai

# Function to encode the image
def encode_image(image_path):
    #This function encodes the image to base64
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

def run(image_folder, api_key):
    # This function takes a folder of images and an API key and returns a list of responses from the GPT-4 Vision model
    openai.api_key = api_key
    # Get a list of the image files
    image_files = os.listdir(image_folder)
    responses = []
    print(image_files)
    # Iterate over the image files
    
    for image_file in image_files:
        print(image_file)
        # Full path to the image file
        image_path = os.path.join(image_folder, image_file)
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
                "text": "You are a powerpoint slide evaluator. Your job is to review the slide and provide feedback on the clarity, simplicity, and visual appeal of the slide. For clarity and simplicity I want you to tell me if the information being presented is given in a direct and pithy way that does not use any extravegant phrasing (extravegant phrasing includes but is not restricted to: 'delve', 'utilize', 'the art and science of', 'enter the world of', etc.). For visual appeal, I want you to tell me if the information on the slide is presented in an effective way. Ensure that you say 1 good thing about the slide, and then provide 3 specific and actionable pieces feedback. Keep responses short and direct yet professional and only consider the text I've given, do not think beyond the slide."
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

        #save the response in a list
        responses.append(response)
        
    return responses