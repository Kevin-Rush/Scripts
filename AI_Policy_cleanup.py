import pandas as pd
import openai
import numpy as np

openai.api_key = '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'

file_path = "C:\\Users\\kevin\\Documents\\Coding\\Scripts\\Cleaned - OECD POLICY LABEL.xlsx"

dfs = pd.read_excel(file_path, sheet_name=None)
df = pd.concat(dfs.values())

df = df.drop(columns=['Original name(s)', 'Acronym', 'Background', 'Target group type(s)', 'Target group(s)', 'Has funding from private sector ?', 'Theme area(s)'])
df = df.loc[:, :'Public access URL']
df = df.loc[:, 'Policy initiative ID':]
df = df.drop(df.columns[11], axis=1)

#drop rows with NaN values in specific columns
df = df.dropna(subset=['Description', 'Objective(s)'])

df['Response'] = np.nan
if not df.index.is_unique:
    df.reset_index(drop=True, inplace=True)

for index, row in df.iterrows():
    prompt = "Hello ChatGPT, I am a policy analyst. I am trying to categorize various AI policies from multiple countries. I have given you a policy descirption and the policy's objectives. Based on this information can you please tell me which category this policy fits into best from this list of categories: \n\nStrategy, Legislation, R&D Programms and Initiatives, Government  Bodies, AI Governance Approach, Education Schemese, Partnerships, Data Initiatives, Resources, Policy Research, Action Plans. \n\nONLY use the material I have given you here and ONLY give it a label I have provided, do not return anything else but the label. \n\nPolicy Description: " + df['Description'][index] + " Policy Objectives: " + df['Objective(s)'][index]
    response = openai.ChatCompletion.create(model="gpt-3.5-turbo", messages=[{"role": "user", "content": prompt}])

    response = response['choices'][0]['message']['content']
    print (response)
    df['Response'][index] = response

print(df.head)

#save df2 to a new csv file
df.to_csv('C:\\Users\\kevin\\Documents\\Coding\\Scripts\\cleaned.csv', index=False)
