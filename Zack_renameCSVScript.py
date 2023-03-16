#Renames data (.csv) to match containing folder's name.
#Note data must be in the following relative directory to .py script: ./Data/X-Name/Raw Data.csv.
import os
x = os.walk("Data")
for i in x:
    if os.path.exists(os.path.abspath(i[0])+"/Raw Data.csv"):
        os.renames(os.path.abspath(i[0])+"/Raw Data.csv", os.path.abspath(i[0])+"/"+i[0][5:]+".csv")
    if os.path.exists(os.path.abspath(i[0])+"/device.csv"):
        os.renames(os.path.abspath(i[0]) + "/device.csv", os.path.abspath(i[0]) + "/" + (i[0].split('\\'))[1] + "-device.csv")
    if os.path.exists(os.path.abspath(i[0])+"/time.csv"):
        os.renames(os.path.abspath(i[0]) + "/time.csv", os.path.abspath(i[0]) + "/" + (i[0].split('\\'))[1] + "-time.csv")