import csv
import json
from openai import OpenAI
from dotenv import load_dotenv
import os
import json


load_dotenv()
gpt_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
client.api_key = gpt_api_key
model = "gpt-4-0125-preview"

exit()

def convert_college_info_to_json(file):
    # this function takes in a text file and converts the text into a json object. Each entry in the json object is a dictionary with the following: category, college_name, infor_url, and info_text
    json_data = []
    with open(file, 'r', encoding='utf-8') as file:
        lines = file.read().split('Complete---------------------')
        messages = [
            {"role": "system", "content": "You are a helpful AI assistant that specializes in clerical tasks such as understanding notes, pulling out key information, and classifying notes. You are currently working in the office of a private company supporting colleges and is trying to keep track of news about the colleges they work with. Therefore, with the wide variety of news stories that you may come across you need to categorize the information as simply as possible, ideally with a single word such as Grant, Event, or Research. These are just examples and you are NOT limited to these 3 options. Please fullfill the needs of the user as best as you can!"},
        ]
#You are a helpful assistant that generates quiz questions based on a topic. Respond with one short question and three plausible options/answers, of which only one is correct. Provide your answer in JSON structure like this {"topic": "<The topic of the quiz>", "question": "<The quiz question you generate>", "options": {"option1": {"body": "<Plausible option 1>", "isItCorrect": <true or false>}, "option2": {"body": "<Plausible option 2>", "isItCorrect": <true or false>}, "option3": {"body": "<Plausible option 3>", "isItCorrect": <true or false>}}}

        for line in lines:
            messages.append({"role": "user", "content": "I'm going to pass you a lengthy note I've made about a college. I need you to provide a JSON object with the following keys: category, college_name, info_url, info_text, and potential action items. You will need to assign the value for category that you think best suits the note. For college name and URL you will find in the note and just need to return that information. As for the info_text, you should return all of the ORIGINAL text that was provided. As for the final entry, potential action items, I need you to return a list of potential follow up actions we can take to . Here is the note:" + line})
            response = client.chat.completions.create(
                model=model,
                response_format={"type": "json_object"},
                messages=messages
            )

            result = json.loads(response.choices[0].message.content)

            print("Processed: ", result["college_name"])
            json_data.append(result)
    return json_data

json_file = convert_college_info_to_json('organized_college_stories.txt')
# Save json_file as a file
with open('new_college_stories.json', 'w', encoding='utf-8') as file:
    json.dump(json_file, file, indent=4)


def json_to_csv(json_file):
    # this function takes in a json file and converts the json object into a csv file
    with open(json_file, 'r') as file:
        json_data = json.load(file)
        with open('AI4WF_stories.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(json_data[0].keys())
            for entry in json_data:
                writer.writerow(entry.values())

def process_log(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        #read the file line by line
        lines = file.readlines()
        lines = [line for line in lines if not line.startswith('RESPONSE: {"searchParameters"')]
        lines = [line for line in lines if line != 'TERMINATE\n']
        lines = [line for line in lines if line != '--------------------------------------------------------------------------------']
        lines = [line for line in lines if line != '\n']
    
    new_file_path = 'new_file.txt'
    with open(new_file_path, 'w', encoding='utf-8') as new_file:
        for line in lines:
            new_file.write(line)

# json_data = clean_notable_college_info('notable_college_info.txt')
# #write json_data to a file
# with open('notable_college_info.json', 'w') as file:
#     json.dump(json_data, file, indent=4)


def clean_log(file):
    # read and write to a file
    with open(file, 'r+', encoding='utf-8') as file:
        lines = file.readlines()
        file.seek(0)  # move the file pointer to the beginning of the file
        # file.truncate()  # clear the file content
        for line in lines:
            line = line.replace('---------------------Search Complete---------------------', '')
            line = line.replace('---------------------Scrape Response---------------------', '')
            line = line.replace('>>>>>>>> EXECUTING FUNCTION google_search...', '')
            line = line.replace('>>>>>>>> EXECUTING FUNCTION web_scraping...', '')
            line = line.replace('Scraping website...', '')
            line = line.replace('''--------------------------------------------------------------------------------\n\n\nTERMINATE\n\n\n--------------------------------------------------------------------------------''', '')
            line = line.replace('0m', '')
            line = line.replace('35m', '')
            line = line.replace('32m', '')
            line = line.replace('33m', '')
            line = line.replace('39m', '')
            line = line.replace('', '')
            line = line.replace('[', '')
            line = line.replace(']', '')
            line = line.replace('਍ഀ', '')
            
            file.write(line)

# def extract_emails(file_path):
#     emails = []
#     i = 0
#     with open(file_path, 'r') as file:
#         reader = csv.reader(file)
#         for row in reader:
#             print(i)
#             print(row[2])
#             if row[0] != "" and row[2] != 'emailAddresses':
#                 emails.append(process_emailAddress_entry(row[2]))  # Assuming email is in the third column (index 2)
#             i += 1
                
#     return emails

# def process_emailAddress_entry(str):
#     #remove all text prior to the @ symbol
#     str = str.split('@')[1]
#     #remove all text after a '
#     str = str.split('\'')[0]
#     return str

def remove_duplicates_list(input):
    #check the datatype of the variable
    if type(input) == list:
        return list(set(input))
    elif type(input) == str:
        if ".txt" in input:
            with open(input, 'r') as file:
                lines = file.readlines()
                return list(set(lines))
    else:
        return input
    
def find_orgs(file):
    orgs = []
    with open(file, 'r') as file:
        reader = csv.reader(file)
        for row in reader:
            if row[0] == 'Organization':
                orgs.append(row[2])  # Assuming organization is in the second column (index 1)
                
    return orgs

full_csv = "contacts-2024-03-25.csv"
orgs = find_orgs(full_csv)

#save emails to a text file
with open('orgs.txt', 'w') as file:
    for org in orgs:
        if org is not None:
            file.write(org + '\n')

# file_path = 'participants.csv' 
# # emails = extract_emails(file_path)
# print(emails)

# emails = remove_duplicates(emails)

# #save emails to a text file
# with open('emails.txt', 'w') as file:
#     for email in emails:
#         if email is not None:
#             file.write(email + '\n')

