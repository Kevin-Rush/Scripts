import json
from openai import OpenAI

def convert_to_json(input_file, output_file, api_key):

    client = OpenAI()
    client.api_key = api_key

    model = "gpt-4"

    with open(input_file, 'r') as file:
        paragraphs = file.read().split('\n\n')  # Split text into paragraphs

    data = []
    for paragraph in paragraphs:
        messages=[
        {"role": "system", "content": "You are an extremely professional expert presentation slide deck writer that has been hired to help write presentations. I will ask you to help me with various tasks such as summarizing a paragraph, generating short and informative titles, writing a conclusion, etc. Please always give the most pithy and direct wording possible without loosing the key information from the text! Berevity and accuracy are key! Please avoid words like utilize or delve or fancy language like exploring the world, mastering the art and science, etc. Additionally, never use colons. Thank you!"}
        ]
        #if data is empty, add the title
        if not data:
            messages.append({"role": "user", "content": "Hello, can you please suggest the best fitting and most direct title for my slide based on the given script? Please make it 3 - 5 words long, and please do not use any colons!"+paragraph.strip()})
            title_completion = client.chat.completions.create(
            model=model,
            messages=messages,
            max_tokens=200
            )
            data.append({
                'title': 'DECK TITLE',
                'subtitle': '',
                'content': title_completion.choices[0].message.content.replace('"', ''), #note, the title entry in JSON is special because the content is the title of the slide and the title key is used as a key in the slide_deck_generator.py file
                'notes': paragraph.strip()
            })
            # data.append({
            #     "title": "LEGAL",
            #     "subtitle": "",
            #     "content": "",
            #     "notes": ""
            # })
            # data.append({
            #     "title": "RECAP",
            #     "subtitle": "",
            #     "content": "",
            #     "notes": ""
            # })
        else:
            messages.append({"role": "user", "content": "Hello, can you please suggest the best fitting and most direct title for my slide based on the given script? For example, if the script is talking about what is going to be discussed during the presentation, a title like Agenda is perfect. However, if one word will not suffice, please make it 3 - 5 words long, and please do NOT use any colons! Here is the script: "+paragraph.strip()})
            title_completion = client.chat.completions.create(model=model, messages=messages, max_tokens=200)
            
            messages.append({"role": "user", "content": "Hello, can you please suggest the best fitting and most direct subtitle for my slide based on the given script and title? Please make it 3 - 5 words long, and please do not use any colons!" + paragraph.strip() + " Please make the subtitle expand on the title but does not repeat the title given here:" + title_completion.choices[0].message.content})
            subtitle_completion = client.chat.completions.create(model=model, messages=messages, max_tokens=200)

            messages.append({"role": "user", "content": "Hello, can you summarize my notes into bullet pionts for a slide deck? Please try to capture the key points of the notes section but DO NOT simply repeat the notes. The bullets should capture the core essence of the key points in the notes while being as brief and pithy as possible. For your context, here is the slide title" + title_completion.choices[0].message.content + " and subtitle: " + subtitle_completion.choices[0].message.content +" here are my notes: " + paragraph.strip() + " Please do not use any colons in your response!"})
            content_completion = client.chat.completions.create(model=model, messages=messages)            
            
            #remove quotation marks from all the completions
            title_completion = title_completion.choices[0].message.content.replace('"', '')
            subtitle_completion = subtitle_completion.choices[0].message.content.replace('"', '')
            content_completion = content_completion.choices[0].message.content.replace('"', '')
            content_completion = content_completion.replace('- ', '')

            # if a colon exists, remove everything to the left of a colon in the title and subtitle
            if ":" in title_completion:
                title_completion = title_completion.split(": ")[-1]
            if ":" in subtitle_completion:
                subtitle_completion = subtitle_completion.split(": ")[-1]

            data.append({
                'title': title_completion,
                'subtitle': subtitle_completion,
                'content': content_completion,
                'notes': paragraph.strip()
            })  # Create a dictionary entry for each paragraph

            #emtpy the messages list
            messages = []

    with open(output_file, 'w') as file:
        json.dump(data, file, indent=4)  # Write data to JSON file