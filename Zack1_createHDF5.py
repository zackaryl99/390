import h5py as h5
import math
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split


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
for i in range(0, 12):
    HDF5File["Jillian"].create_dataset(str(i) + "-Jillian",
                                       data=np.genfromtxt("./Data/" + str(i) + "-Jillian/" + str(i) + "-Jillian.csv",
                                                          delimiter=','))
    HDF5File["Zack"].create_dataset(str(i) + "-Zack",
                                    data=np.genfromtxt("./Data/" + str(i) + "-Zack/" + str(i) + "-Zack.csv",
                                                       delimiter=','))
    HDF5File["Zeerak"].create_dataset(str(i) + "-Zeerak",
                                      data=np.genfromtxt("./Data/" + str(i) + "-Zeerak/" + str(i) + "-Zeerak.csv",
                                                         delimiter=','))

# To create the 5-second windows, we will go through each of the original .csv files, and copy 5-second segments into
# their own datasets (create a list of 5-second datasets), then split and shuffle that list of datasets between train and test.

# We will have a lot of overlap between windows by only jumping 100 csv lines between windows.

# First create a dictionary which associates each key with the name of the containing group (team member name)
# Then create a list of those keys which we can iterate over
allDatasetDict = {}
nameList = ["Jillian", "Zack", "Zeerak"]
for name in nameList:
    for key in HDF5File[name].keys():
        allDatasetDict[key] = name
allDatasetKeys = list(allDatasetDict.keys())

# Go through each 1-minute dataset and extract many 5-second windows into their own datasets
winList = [] # List of 5-second windows (tables)
overlap = 200  # This is how much the window "jumps" forward each time. Increase for fewer windows
for key in allDatasetKeys:
    lines = HDF5File[allDatasetDict[key]][key].shape[0]  # Number of lines in this dataset
    src = HDF5File[allDatasetDict[key]][key]  # Pointer to source dataset (easier than using that hdf5file thing)
    start = 0  # Starting index always 0
    end = int(math.floor(lines / 12))  # Guess of where first "end" will be (60seconds / 12 ~= 5 seconds)

    while end < lines:  # While our window doesn't overflow EOF
        if src[end, 0] - src[start, 0] < 5:  # Increment window until it's JUST under 5 seconds long
            end += 1
            continue
        winList.append(src[start:end, :])  # Add this window to list of windows
        start += overlap
        end += overlap - 2  # This is so that we are under 5 seconds again, and iterate to find closest window to 5 seconds

# Randomly split windows into train and test sets (and shuffle windows)
train, test = train_test_split(winList, train_size=0.9, random_state=69, shuffle=True)

# Create dataset for each 5-second training window
index = 0
for wnd in train:
   HDF5File["dataset/Train"].create_dataset("train_" + str(index), data=wnd)
   index += 1

# Create dataset for each 5-second testing window
index = 0
for wnd in test:
   HDF5File["dataset/Test"].create_dataset("test_" + str(index), data=wnd)
   index += 1

# Debug: check that duration of a random window is ~5 seconds and number of keys in test (~10%)
print(len(HDF5File["dataset/Test"].keys()))

src = HDF5File["dataset/Test/test_2"]
print(src[:,:])
print(src.shape[0])
print(str(src[src.shape[0]-1,0] - src[0,0]))

print("Total windows: ")
print(str(len(HDF5File["dataset/Test"].keys())+len(HDF5File["dataset/Train"].keys())))
