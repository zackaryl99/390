import h5py as h5
import math
import random
import numpy as np
import pandas as pd

# Seed random (used for randomly splitting data into test vs train)
random.seed()

# Create HDF5 file (root)
HDF5File = h5.File("data.hdf5", 'w')

# This is all to get key list in random order, but hdf5 seems to alphabetically order datasets in a group...
allDatasetDict = {}
nameList = ["Jillian", "Zack", "Zeerak"]
for name in nameList:
   for key in HDF5File[name].keys():
      allDatasetDict[key] = name
allDatasetKeys = list(allDatasetDict.keys()) # random order of keys which reference dict
random.shuffle(allDatasetKeys)
print("total of " + str(len(allDatasetKeys)) + " original datasets")