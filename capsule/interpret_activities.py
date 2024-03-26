import pandas as pd
import numpy as np

def get_org(full_name):
    #read the participants.csv file
    df = pd.read_csv('participants.csv')
    if type(full_name) == str:
        first_name = full_name.split(' ')[0]
        last_name = full_name.split(' ')[1]
        for i in range(len(df)):
            if df['firstName'][i] == first_name and df['lastName'][i] == last_name:
                return df['organisation'][i]
    
    return None

# Read the CSV file into a data frame
df = pd.read_csv('report_of_activities.csv')

print(df.columns)
df = df[['Contact Id', 'Contact Name', 'Type', 'Entry Id', 'Date', 'Content']]

#remove all nan values from the df
df = df.dropna()

#add new column to df
df['Organization_Name'] = ""

for i in range(len(df)):
    if df.iloc[i]['Type'] == 'Organization':
        df.at[i, 'Organization_Name'] = df.iloc[i]['Contact Name']
    else:
        print(df.iloc[i]['Contact Name'])
        df.at[i, 'Organization_Name'] = get_org(df.iloc[i]['Contact Name'])

print(df.head())

#save the df to csv file
df.to_csv('report_of_activities.csv', index=False)

df_org_info = pd.DataFrame()
#run through the df add each org_name to a list
org_names = df['Organization_Name'].unique()

#create a dataframe where each column is an engtry in org_names
for org in org_names:
    df_org_info[org] = np.zeros(1)

#run through df and add the content to the respective org_name column
for i in range(len(df)):
    org_name = df.iloc[i]['Organization_Name']
    content = df.iloc[i]['Content']
    #add content to the first entry of the org_name column
    if df_org_info.at[0, org_name] == np.nan:
        df_org_info.at[0, org_name] = content
    else:
        df_org_info.at[0, org_name] = str(df_org_info.iloc[0][org_name]) + str(content)


#save the df_org_info to csv file
df_org_info.to_csv('org_info.csv', index=False)