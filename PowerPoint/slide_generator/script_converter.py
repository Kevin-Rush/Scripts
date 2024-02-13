import json
import openai

def convert_to_json(input_file, output_file, api_key):

    openai.api_key = api_key
    messages=[
        {"role": "system", "content": "You are a helpful slide deck writing that is helping me write a presentation. I will ask you to help me with various tasks such as summarizing a paragraph, generating short and informative titles, writing a conclusion, etc. Please always give the most pithy and direct wording possible without loosing the key information from the text! Berevity and accuracy are key! Please avoid words like utilize or delve or fancy language like exploring the world, mastering the art and science, etc. Additionally, never use colons. Thank you!"}
    ]

    with open(input_file, 'r') as file:
        paragraphs = file.read().split('\n\n')  # Split text into paragraphs

    data = []
    for paragraph in paragraphs:
        #if data is empty, add the title
        if not data:
            messages.append({"role": "user", "content": "Hello, can you please capture the essence of my slide script to generate a direct and relevant title for this slide?"+paragraph.strip()})
            title_completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=messages,
            )

            data.append({
                'title': 'DECK TITLE',
                'subtitle': '',
                'content': title_completion['choices'][0]['message']['content'].replace('"', ''), #note, the title entry in JSON is special because the content is the title of the slide and the title key is used as a key in the slide_deck_generator.py file
                'notes': paragraph.strip()
            })
            data.append({
                "title": "LEGAL",
                "subtitle": "",
                "content": "",
                "notes": ""
            })
            data.append({
                "title": "RECAP",
                "subtitle": "",
                "content": "",
                "notes": ""
            })
        else:
            messages.append({"role": "user", "content": "Hello, can you please capture the essence of my slide script to generate a direct and relevant title for this slide?"+paragraph.strip()})
            title_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            
            messages.append({"role": "user", "content": "Hello, can you please capture the essence of my slide script to generate a direct and relevant subtitle for this slide? " + paragraph.strip() + " Please make the subtitle informative but different from the title." + title_completion['choices'][0]['message']['content']})
            subtitle_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)

            messages.append({"role": "user", "content": "Hello, can you summarize my notes from this slide in bullet points? Please try to capture the key points of the notes section but DO NOT simply repeat the notes. All bullets should capture the same meaning of the key points while saying it in a unique way. For your context, here is the slide title" + title_completion['choices'][0]['message']['content'] + " and subtitle: " + subtitle_completion['choices'][0]['message']['content'] +" here are my notes: " + paragraph.strip()})
            content_completion = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=messages)
            #remove quotation marks from the content
            content_completion['choices'][0]['message']['content'] = content_completion['choices'][0]['message']['content'].replace('"', '')
            data.append({
                'title': title_completion['choices'][0]['message']['content'].replace('"', ''),
                'subtitle': subtitle_completion['choices'][0]['message']['content'].replace('"', ''),
                'content': content_completion['choices'][0]['message']['content'].replace('- ', ''),
                'notes': paragraph.strip()
            })  # Create a dictionary entry for each paragraph

    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)  # Write data to JSON file

# Usage example
input_file = r'C:\Users\kevin\Documents\Coding\Scripts\PowerPoint\slide_generator\scripts\SIP_script.txt'
output_file = r'C:\Users\kevin\Documents\Coding\Scripts\PowerPoint\slide_generator\json_scripts\SIP_script.json'

with open("C:/Users/kevin/Documents/Coding/Scripts/gpt_api_key.txt", "r") as file:
    api_key = file.read()

convert_to_json(input_file, output_file, api_key)