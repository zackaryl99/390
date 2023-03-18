import h5py as h5
import math
import random
import numpy as np

def make5(dataset):
   dataset.resize(dataset.shape[0] + 1, axis=0)
   dataset[dataset.shape[0] - 1, 0] = dataset[0, 0] + 5
   for i in range(1, 6):
      dataset[dataset.shape[0] - 1, i] = dataset[dataset.shape[0] - 2, i]

# Seed random (used for randomly splitting data into test vs train)
random.seed()

# Create HDF5 file (root)
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
   HDF5File["Jillian"].create_dataset(str(i)+"-Jillian", data=np.genfromtxt("./Data/"+str(i)+"-Jillian/"+str(i)+"-Jillian.csv", delimiter=','))
   HDF5File["Zack"].create_dataset(str(i)+"-Zack", data=np.genfromtxt("./Data/"+str(i)+"-Zack/"+str(i)+"-Zack.csv", delimiter=','))
   HDF5File["Zeerak"].create_dataset(str(i)+"-Zeerak", data=np.genfromtxt("./Data/"+str(i)+"-Zeerak/"+str(i)+"-Zeerak.csv", delimiter=','))


# This is all to get key list in random order, but hdf5 seems to alphabetically order datasets in a group...
allDatasetDict = {}
nameList = ["Jillian", "Zack", "Zeerak"]
for name in nameList:
   for key in HDF5File[name].keys():
      allDatasetDict[key] = name
allDatasetKeys = list(allDatasetDict.keys()) # random order of keys which reference dict
random.shuffle(allDatasetKeys)


# Split 60 second datasets into (roughly) 5 second windows. I chose to only extract 55 seconds from each 60 second dataset
end = 0
windowCount = 0 # counts how many windows (5-seconds) are created
durations = []

for key in allDatasetKeys:
   lineCount = HDF5File[allDatasetDict[key]][key][()].shape[0]  # number of lines in this dataset
   srcDataset = HDF5File[allDatasetDict[key]][key]  # the dataset in question
   for k in range(0, 11):
      windowCount = windowCount + 1  # one more window made
      start = end + 1  # The starting line index for this window
      end = int(end + math.floor(lineCount/12)) # estimated ending line index for this window
      lastDur = 0  # Will hold duration of previous iteration's window
      thisDur = srcDataset[end][0] - srcDataset[start][0]  # duration of first iteration's window
      while 5.0-thisDur > 0:  # get as close as possible to 5 seconds, without going over
         end = end + 1  # still less than 5? try incrementing
         lastDur = thisDur  # duration of (now) previous window (so time at end line minus time at starting line)
         thisDur = srcDataset[end][0] - srcDataset[start][0]
      end = end - 1  # previous loop failed, so must have gone one line too far
      durations.append(srcDataset[end][0] - srcDataset[start][0])  # Used to calculate average window size before forcing to 5 seconds
      if random.random() >=0.1:  # split test and training data
         # Make new 5-second window from slice of larger 60-second dataset and make it resizeable
         HDF5File["dataset/Train"].create_dataset(key + "-Window" + str(k), data=srcDataset[start:end, :], maxshape=(None, None))
      else:
         HDF5File["dataset/Test"].create_dataset(key + "-Window" + str(k), data=srcDataset[start:end, :], maxshape=(None, None))
   end = 0

# Make windows EXACTLY 5 seconds
for key in HDF5File["dataset/Train"].keys():  # for each 5-second window in Training
   make5(HDF5File["dataset/Train"][key])
for key in HDF5File["dataset/Test"].keys():  # for each 5-second window in Testing
   make5(HDF5File["dataset/Test"][key])


# This stuff just computes average window length before and after forcing it to be 5 seconds EXACTLY
sum = 0
for val in durations:
   sum = sum + val
print("old average duration of window: " + str(float(sum/windowCount)))

sum = 0
for key in list(HDF5File["dataset/Train"].keys()):
    dataset = HDF5File["dataset/Train"][key]
    sum += dataset[dataset.shape[0]-1][0]-dataset[0][0]

for key in list(HDF5File["dataset/Test"].keys()):
   dataset = HDF5File["dataset/Test"][key]
   sum += dataset[dataset.shape[0] - 1][0] - dataset[0][0]

print("new average duration of window: " + str(float(sum/windowCount)))
