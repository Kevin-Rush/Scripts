import pandas as pd


data = pd.read_csv(r'C:\Users\kevin\Documents\Personal\Athletics\SmartWatchData\SLEEP_1666271863586.csv')
data = data.iloc[:,:-21] #Get rid of the 21 unammed columns at the end of the csv file

for x in data.index:
    if data.loc[x, "start"] == data.loc[x, "stop"]: #sleep start and end date are the same, therefore a bad entry
        data.drop(x, inplace = True)#remove bad entry
    
print(data.head())

data.start = data.start.replace(r'\+0000', '', regex=True)
data.stop = data.stop.replace(r'\+0000', '', regex=True)


print(data.head())