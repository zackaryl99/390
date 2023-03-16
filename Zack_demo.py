import h5py as h5
import numpy as np
import math
import random

# Seed random (used for randomly splitting data into test vs train)
random.seed()

# Open HDF5
HDF5File = h5.File("data.hdf5", 'r')

# Verification
print("Level 1 Groups: "+str(HDF5File.keys()))

# Create list of keys in each group (makes it easier to index keys group[4] if theyre in a list like this)
keyList = [key for key in HDF5File["dataset/Train"].keys()]


i = 0

for key in keyList:
   lines = HDF5File["dataset/Train"][key][()].shape[0]
   span = HDF5File["dataset/Train"][key][lines-1][0]-HDF5File["dataset/Train"][key][0][0]
   print("--+-- " + key + " --+--")
   print("Number of lines: " + str(lines))
   print("Total duration: " + str(span))
   print("Data collection rate: " + str(lines/span))



   # print("First time-point: " + str(HDF5File["Jillian"][keyList[i]][0][0]))
   # print("First line: " + str(HDF5File["Jillian"][keyList[i]][0]))
   #
   # print("Last time-point: " + str(HDF5File["Jillian"][keyList[i]][last-1][0]))
   # print("Last line: " + str(HDF5File["Jillian"][keyList[i]][last-1]))
# print("Contents of \"" + str(keyList[4]) + "\": "+str(HDF5File["Jillian"][keyList[4]][()].shape[0]))
# print("Shape of \"" + str(testKeys[4]) + "\": "+str(HDF5File["dataset/Test"][testKeys[4]].shape))

