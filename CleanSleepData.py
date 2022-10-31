from tkinter.tix import Tree
import pandas as pd
import math

data = pd.read_csv(r'C:\Users\kevin\Documents\Personal\Athletics\SmartWatchData\SLEEP_1666271863586.csv')
data = data.iloc[:,:-21] #Get rid of the 21 unammed columns at the end of the csv file
data['naps'] = data['naps'].fillna(0)
#print(data.head())


for x in data.index:
    if data.loc[x, 'naps'] != 0:
        data.loc[x, 'naps']= str(data.loc[x, 'naps'])[23:-7]
    if data.loc[x, 'start'] == data.loc[x, 'stop']: #sleep start and end date are the same, therefore a bad entry
        data.drop(x, inplace = True)#remove bad entry

data.start = data.start.replace(r'\+0000', '', regex=True)
data.stop = data.stop.replace(r'\+0000', '', regex=True)

print(data)

data['totalSleepTime'] = round((data['deepSleepTime'] + data["shallowSleepTime"] + data["REMTime"])/60, 2) #add up all sleep time, create new culumn and round to 2 decimals

print(data)
