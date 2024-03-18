from colorama import Fore
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

response = requests.get(parties_url, headers=headers)
if response.status_code != 200:
    print(f'Request failed with status code {response.status_code}')
    exit()
print('Successful Request: ', response.status_code)

data = response.json()

#save the extracted json data in a df
df_parties = pd.DataFrame(data['parties'])

#print the comolumns in the df
print("columns: ", df_parties.columns)
print(df_parties.head(1))

#create an empty df
df = pd.DataFrame()

for i in range(len(df_parties)):
    print()
    print("df_parties id: ", df_parties["id"][i])

    entity = "parties"
    entityId = df_parties["id"][i]
    print("entityId: ", entityId)

    entries_url = f"https://api.capsulecrm.com/api/v2/{entity}/{entityId}/entries"

    response = requests.get(entries_url, headers=headers)
    if response.status_code != 200:
        print(f'Request failed with status code {response.status_code}')
        exit()
    print('Successful Request: ', response.status_code)

    data = response.json()
    print("data: ", data)
    df_entries = pd.DataFrame(data['entries'])
    print("columns: ", df_entries.columns)
    print(df_entries.head(1))

    #check if df_entries is not empty
    if not df_entries.empty:
        print(f"{Fore.YELLOW}---------------------Entry Found---------------------{Fore.RESET}")
        print(df_entries["activityType"])
        print(df_entries["type"])
        #if the activityType series contains "Note"
        if df_entries["type"][0] == "note":
            print(f"{Fore.GREEN}---------------------Note Added---------------------{Fore.RESET}")
            df = df.append(df_entries["content"], ignore_index=True)
            print("note: ", df_entries["content"])
#save the df to a csv file
df.to_csv('activity.csv', index=False)
print('Activity saved to activity.csv')