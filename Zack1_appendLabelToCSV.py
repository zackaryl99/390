import pandas as pd

dataframes = {}

for i in range(0,12):  # Create dataFrames from 60-second datasets
    dataframes[i+1000] = (pd.read_csv("./Data/"+str(i)+"-Jillian/"+str(i)+"-Jillian.csv", delimiter=',', skiprows=0))
    dataframes[i+2000] = (pd.read_csv("./Data/"+str(i)+"-Zack/"+str(i)+"-Zack.csv", delimiter=',', skiprows=0))
    dataframes[i+3000] = (pd.read_csv("./Data/"+str(i)+"-Zeerak/"+str(i)+"-Zeerak.csv", delimiter=',', skiprows=0))

for df in dataframes:  # Add label to each 60-second window (0 = walking, 1 = jumping)
    if df % 1000 < 6:
        dataframes[df].insert(5,'label','0')
    else:
        dataframes[df].insert(5, 'label', '1')

for i in range(0,12):  # Write back to csv (overwrite)
    dataframes[i+1000].to_csv("./Data/"+str(i)+"-Jillian/"+str(i)+"-Jillian.csv",index=False,header=False)
    dataframes[i+2000].to_csv("./Data/"+str(i)+"-Zack/"+str(i)+"-Zack.csv",index=False,header=False)
    dataframes[i+3000].to_csv("./Data/"+str(i)+"-Zeerak/"+str(i)+"-Zeerak.csv",index=False,header=False)