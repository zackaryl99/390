import os
import pandas as pd

# os.makedirs("./TESTDIR")

dataframes = {}

for i in range(0,12):
    dataframes[i+1000] = (pd.read_csv("./Data/"+str(i)+"-Jillian/"+str(i)+"-Jillian.csv", delimiter=',', skiprows=0))
    dataframes[i+2000] = (pd.read_csv("./Data/"+str(i)+"-Zack/"+str(i)+"-Zack.csv", delimiter=',', skiprows=0))
    dataframes[i+3000] = (pd.read_csv("./Data/"+str(i)+"-Zeerak/"+str(i)+"-Zeerak.csv", delimiter=',', skiprows=0))

# for df in dataframes:
#     print(dataframes[df].shape)
# print(type(dataframes))
# print(len(dataframes))
print(dataframes.keys())

for df in dataframes:
    if df % 1000 < 6:
        dataframes[df].insert(5,'label','0')
    else:
        dataframes[df].insert(5, 'label', '1')

print(dataframes[1000])
for i in range(0,12):
    # os.makedirs("./TESTDIR/"+str(i)+"-Jillian/")
    # os.makedirs("./TESTDIR/" + str(i) + "-Zack/")
    # os.makedirs("./TESTDIR/" + str(i) + "-Zeerak/")
    dataframes[i+1000].to_csv("./Data/"+str(i)+"-Jillian/"+str(i)+"-Jillian.csv",index=False,header=False)
    dataframes[i+2000].to_csv("./Data/"+str(i)+"-Zack/"+str(i)+"-Zack.csv",index=False,header=False)
    dataframes[i+3000].to_csv("./Data/"+str(i)+"-Zeerak/"+str(i)+"-Zeerak.csv",index=False,header=False)