import requests
import pandas as pd

#read the api token from the capsule_api.txt file
with open("capsule_api_key.txt", "r") as file:
    api_token = file.read()


headers = {
    'Authorization': f'Bearer {api_token}',
    'Accept': 'application/json'
}
parties_url = 'https://api.capsulecrm.com/api/v2/parties'

activity_url = 'https://api.capsulecrm.com/api/v2/activitytypes'

response = requests.get(parties_url, headers=headers)
if response.status_code != 200:
    print(f'Request failed with status code {response.status_code}')
    exit()
print('Successful Request: ', response.status_code)

data = response.json()

#save the extracted json data in a df
df = pd.DataFrame(data['parties'])

#print the comolumns in the df
print("columns: ", df.columns)
print(df.head())

#for i in range(len(df["id"])):
#print("df id: ", df["id"][i])

entity = "parties"
entityId = 230533890
print("entityId: ", entityId)

entries_url = f"https://api.capsulecrm.com/api/v2/{entity}/{entityId}/entries"

response = requests.get(entries_url, headers=headers)
if response.status_code != 200:
    print(f'Request failed with status code {response.status_code}')
    exit()
print('Successful Request: ', response.status_code)

data = response.json()
print("data: ", data)
#save the extracted json data in a df
temp_df = pd.DataFrame(data["entries"])

#print the comolumns in the df
print("columns: ", temp_df.columns)

print(temp_df.head(1))
