import requests
import pandas as pd

#read the api token from the capsule_api.txt file
with open("capsule_api_key.txt", "r") as file:
    api_token = file.read()

def internal_email_check(email):
    #read a file of internal email addresses and check if email matches any
    with open("internal_emails.txt", "r") as file:
        internal_emails = file.read().splitlines()
    email = email.split('@')[1]
    if email in internal_emails:
        print(f"Internal email found: {email}")
        return True
    return False

headers = {
    'Authorization': f'Bearer {api_token}',
    'Accept': 'application/json'
}

#read the party_ids.txt file and create a list of party ids
with open("party_ids.txt", "r") as file:
    party_ids = file.read().splitlines()

df = pd.DataFrame()
for id in party_ids:
    url = f'https://api.capsulecrm.com/api/v2/parties/{id}'
    print(url)
    response = requests.get(url, headers=headers)
    if response.status_code != 200:
        print(f'Request failed with status code {response.status_code}')
    data = response.json()
    print(data)
if data['party']['type'] != 'organisation':
        if data['party']['emailAddresses'] != []:
            email = data['party']['emailAddresses'][0]['address']
            if not internal_email_check(email):
                df_temp = pd.DataFrame([data['party']])
                df = df.append(df_temp, ignore_index=True)
        else:
            df_temp = pd.DataFrame([data['party']])
            df = df.append(df_temp, ignore_index=True)
    # print(df.columns)
    # print(df.head(1))
#save first name, last name, and email to a csv file

df = df[['id', 'firstName', 'lastName', 'organisation', 'emailAddresses']]
print(df.head())
for i in range(len(df['emailAddresses'])):
    if df['emailAddresses'][i] != []:
        df['emailAddresses'][i] = df['emailAddresses'][i][0]["address"]

for i in range(len(df['organisation'])):
    if df['organisation'][i] != None:
        df['organisation'][i] = df['organisation'][i]["name"]
print(df.head())

df.to_csv('participants.csv', index=False)
print('Emails saved to participants.csv')

