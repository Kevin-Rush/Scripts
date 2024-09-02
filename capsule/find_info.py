import csv
import pandas as pd
from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
gpt_api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI()
client.api_key = gpt_api_key

filename = 'extracted_log_data.csv'

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

for i, row in df.iloc[1:].iterrows():
    if row[1] is None:
        continue
    else:
        messages.append(
            {"role": "user",
                "content": f"What is the number of gradutes for {row[0]}? Please return '0 graduates for {row[0]}' if you cannot find the number in the attached log. Again, DO NOT provide any additional information if the number is NOT found; just say '0 graduates for {row[0]}'!"
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

output_filename = 'response_list.csv'

with open(output_filename, 'w', newline='') as file:
    writer = csv.writer(file)
    writer.writerow(['Response'])
    writer.writerows([[response] for response in response_list])