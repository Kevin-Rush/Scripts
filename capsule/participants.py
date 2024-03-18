import requests
import pandas as pd

#read the api token from the capsule_api.txt file
with open("capsule_api.txt", "r") as file:
    api_token = file.read()


headers = {
    'Authorization': f'Bearer {api_token}',
    'Accept': 'application/json'
}
url = 'https://api.capsulecrm.com/api/v2/parties'

response = requests.get(url, headers=headers)

if response.status_code == 200:
    print('Request was successful')
    data = response.json()
    #save the extracted json data in a df
    df = pd.DataFrame(data['parties'])
    print(df.head())

else:
    print(f'Request failed with status code {response.status_code}')
