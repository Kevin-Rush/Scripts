import requests
import pandas as pd

#read the api token from the capsule_api.txt file
with open("capsule_api_key.txt", "r") as file:
    api_token = file.read()


headers = {
    'Authorization': f'Bearer {api_token}',
    'Accept': 'application/json'
}
url = 'https://api.capsulecrm.com/api/v2/activitytypes'

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print('Successful Request')
    data = response.json()
    #save the extracted json data in a df
    df = pd.DataFrame(data['activityTypes'])
    
    #print the comolumns in the df
    print(df.columns)

    print(df.head(1))

else:
    print(f'Request failed with status code {response.status_code}')
