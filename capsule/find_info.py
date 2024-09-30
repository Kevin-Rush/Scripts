import csv
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
gpt_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
client.api_key = gpt_api_key

directories = ['0908_Stories', '0908_AMD', '0908_AWS', '0908_Microsoft']

df = pd.DataFrame(columns=['college', 'log_type', 'info_found'])

messages = [
            {"role": "system", 
                "content": "You are a helpful assistant that excels at reading log files from an AI search agent to find key information. These log files only contain the responses from the agent NOT the prompts from their manager. Therefore, you will see the results of multiple searches without context of what prompted that search. Therefore, the agent may say they found nothing, but in a later search found relevant information. Therefore, when responding to a prompt, always consider the ENTIRE LOG to when replying. Please be very attentive when reading through log files and responding to the user's questions and only provide the information found in the log file. The user's job is depending on you!"}
        ]

for directory in directories:
    for filename in os.listdir(directory):
        filepath = os.path.join(directory, filename)

        with open(filepath, 'r') as file:
            file_content = file.read()

        college = filename.split('_')[-1].split('.')[0]
        log_type = directory.split('_')[-1]

        if log_type == 'Stories':
            messages.append(
                {"role": "user",
                    "content": f"Does the log file for {college} contain any information about student success stories, or does the log file indicate that nothing was found? Even the littest piece of information is helpful! Please respond with 'Information found for {college}' or 'No information found for {college}' Here is the log file: {file_content}"
                })
        elif log_type == 'AMD':
            messages.append(
                {"role": "user",
                    "content": f"Does the log file for {college} contain any information about AMD collaborating with {college}, or does the log file indicate that nothing was found? Even the littest piece of information is helpful! Please respond with 'Information found for {college}' or 'No information found for {college}' Here is the log file: {file_content}"
                })
        elif log_type == 'AWS':
            messages.append(
                {"role": "user",
                    "content": f"Does the log file for {college} contain any information about AWS collaborating with {college}, or does the log file indicate that nothing was found? Even the littest piece of information is helpful! Please respond with 'Information found for {college}' or 'No information found for {college}' Here is the log file: {file_content}"
                })
        elif log_type == 'Microsoft':
            messages.append(
                {"role": "user",
                    "content": f"Does the log file for {college} contain any information about Microsoft collaborating with {college}, or does the log file indicate that nothing was found? Even the littest piece of information is helpful! Please respond with 'Information found for {college}' or 'No information found for {college}' Here is the log file: {file_content}"
                })
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        messages.pop()

        response = response.choices[0].message.content

        print(response)
        df = df.append({'college': college, 'log_type': log_type, 'info_found': response}, ignore_index=True)

df.to_csv('0908_search_info.csv', index=False)
exit()

        

#to be used for csv files
with open(filename, 'r') as file:
    reader = csv.reader(file)
    rows = list(reader)
    df = pd.DataFrame(rows)

college_column = [row[0] for row in rows]

messages = [
            {"role": "system", 
                "content": "You are a helpful assistant that excels at reading log files and finding key information."}
        ]

response_list = []

# target_college = 'State of Arkansas'
# target_row = df[df[0] == target_college]

# print(target_row)
# for entry in target_row.values[0]:
#     print(len(entry))

# print(df.iloc[89].values[0])

# exit()

for i, row in df.iloc[90:].iterrows():
    if row[1] is None:
        continue
    else:
        messages.append(
            {"role": "user",
                "content": f"What is the number of students that received certificates in AI for {row[0]}? Please return '0 graduates for {row[0]}' if you cannot find the number in the attached log. Again, DO NOT provide any additional information if the number is NOT found; just say '0 certificates awarded from {row[0]}'!"
            })
        messages.append({"role": "user", 
                         "content": f"Here is the log file: {row[1]}"})
        
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=messages,
        )

        messages.pop()

        response = response.choices[0].message.content

        print(response)
        response_list.append(response)
