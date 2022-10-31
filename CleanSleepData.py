import pandas as pd


data = pd.read_csv(r'C:\Users\kevin\Documents\Personal\Athletics\SmartWatchData\SLEEP_1666271863586.csv')
data = data.iloc[:,:-21] #Get rid of the 21 unammed columns at the end of the csv file

for x in data.index:
    print(data.loc[x, "start"])
    if data.loc[x, "start"] == data.loc[x, "stop"]: #sleep start and end date are the same, therefore a bad entry
        data.drop(x, inplace = True)#remove bad entry
    
    


print(data.head())