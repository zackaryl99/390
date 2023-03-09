import h5py as h5
import numpy as np
import math
import random

# Seed random (used for randomly splitting data into test vs train)
random.seed()

#Create HDF5 file (root)
HDF5File = h5.File("data.hdf5", 'w')

# Create Level 1 Groups
HDF5File.create_group("Jillian")
HDF5File.create_group("Zack")
HDF5File.create_group("Zeerak")
HDF5File.create_group("dataset")

# Create Level 2 Groups
HDF5File["dataset"].create_group("Train")
HDF5File["dataset"].create_group("Test")

# Populate each individual's group with their datasets, by creating a Numpy array from .csv files.
for i in range(0,12):
   HDF5File["Jillian"].create_dataset(str(i)+"-Jillian", data=np.genfromtxt("./Data/"+str(i)+"-Jillian/"+str(i)+"-Jillian.csv", delimiter=',')[1:, :])
   HDF5File["Zack"].create_dataset(str(i)+"-Zack", data=np.genfromtxt("./Data/"+str(i)+"-Zack/"+str(i)+"-Zack.csv", delimiter=',')[1:, :])
   HDF5File["Zeerak"].create_dataset(str(i)+"-Zeerak", data=np.genfromtxt("./Data/"+str(i)+"-Zeerak/"+str(i)+"-Zeerak.csv", delimiter=',')[1:, :])

# Populate "Train" group with 5-second windows (12 [datasets/person] * 3 [person] * 12 [windows/dataset] = 432 [datasets])
# Note: this scirpt doesn't produce EXACT 5 second clips, rather it counts the number of lines, divides by 12 (60 seconds / 12 = 5 seconds) and divides the dataset in 12 according to those partitions
count = 0
nameList = ["Jillian", "Zack", "Zeerak"]
for i in range(0,3): #for each name
   for j in range(0,12): #for each file
      with open(r"./Data/"+str(j)+"-"+nameList[i]+"/"+str(j)+"-"+nameList[i]+".csv", 'r') as fp:
         count = sum(1 for line in fp)
      for k in range(0, 12): #for each subset of data (5s windows)
         if (random.random() >=0.1):
            HDF5File["dataset/Train"].create_dataset(str(j)+"-"+nameList[i]+"-Window" + str(k), data=np.genfromtxt("./Data/"+str(j)+"-"+nameList[i]+"/"+str(j)+"-"+nameList[i]+".csv", delimiter=',')[int(k*(math.floor(count)/12)+1):int((k+1)*(math.floor(count)/12)), :])
         else:
            HDF5File["dataset/Test"].create_dataset(str(j)+"-"+nameList[i]+"-Window" + str(k), data=np.genfromtxt("./Data/"+str(j)+"-"+nameList[i]+"/"+str(j)+"-"+nameList[i]+".csv", delimiter=',')[int(k*(math.floor(count)/12)+1):int((k+1)*(math.floor(count)/12)), :])
      count = 0



# Verification
print("Level 1 Groups: "+str(HDF5File.keys()))
print("Contents of Jillian: "+str(HDF5File["Jillian"].keys()))
print("Contents of Zack: "+str(HDF5File["Zack"].keys()))
print("Contents of Zeerak: "+str(HDF5File["Zeerak"].keys()))
print("Number of keys in Train (expecting ~389): "+str(len(HDF5File["dataset/Train"].keys())))
print("Number of keys in Test (expecting ~44): "+str(len(HDF5File["dataset/Test"].keys())))

# Create list of keys in each group (makes it easier to index keys group[4] if theyre in a list like this)
trainKeys = [key for key in HDF5File["dataset/Train"].keys()]
testKeys = [key for key in HDF5File["dataset/Test"].keys()]

print("Contents of \"" + str(testKeys[4]) + "\": "+str(HDF5File["dataset/Test"][testKeys[4]][()]))
print("Shape of \"" + str(testKeys[4]) + "\": "+str(HDF5File["dataset/Test"][testKeys[4]].shape))
#print("Contents of \"" + str(trainKeys[3]) + "\": "+str(HDF5File["dataset/Train"][trainKeys[3]][()]))
#print("Contents of \"" + str(testKeys[4]) + "\": "+str(HDF5File["dataset/Test"][testKeys[4]][()]))

#print("Shape of \"4-Zack\": "+str(HDF5File["Zack"]["4-Zack"].shape))
#print("Shape of \"3-Jillian-Window6\": "+str(HDF5File["dataset/Train"]["3-Jillian-Window6"].shape))
#print("Contents of \"" + str(HDF5File["dataset/Train"].keys()) + "\": "+str(HDF5File["dataset/Train"][2][()]))
