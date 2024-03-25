import requests
import pandas as pd

#read the api token from the capsule_api.txt file
with open("capsule_api_key.txt", "r") as file:
    api_token = file.read()


headers = {
    'Authorization': f'Bearer {api_token}',
    'Accept': 'application/json'
}

# success = True
# i = 1
# df = pd.DataFrame()
# while success == True:

# url = f'https://api.capsulecrm.com/api/v2/parties'
# print(url)
# i += 1

# response = requests.get(url, headers=headers)

# if response.status_code != 200:
#     print(f'Request failed with status code {response.status_code}')
#     # success = False

# print('Successful Request')
# data = response.json()
# #print(data)


# #add the extracted json to the df
# df = pd.DataFrame(data['parties'])
# # print(len(df))

#print the comolumns in the df
#print(df.columns)

# print(df.head(-1))

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
    if data['party']['type'] != 'organization':
        df_temp = pd.DataFrame([data['party']])
        df = df.append(df_temp, ignore_index=True)
    # print(df.columns)
    # print(df.head(1))
#save first name, last name, and email to a csv file

df = df[['firstName', 'lastName', 'emailAddresses']]
print(df.head())
for i in range(len(df['emailAddresses'])):
    if df['emailAddresses'][i] != []:
        df['emailAddresses'][i] = df['emailAddresses'][i][0]["address"]
print(df.head())

df.to_csv('participants.csv', index=False)
print('Emails saved to participants.csv')

