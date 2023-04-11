import h5py as h5
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# Create HDF5 file (root)
HDF5File = h5.File("data.hdf5", 'r')

features_train = pd.DataFrame(columns=['meanABS', 'stdABS', 'maxABS', 'kurtosisABS', 'skewABS', 'label'])
features_test = pd.DataFrame(columns=['meanABS', 'stdABS', 'maxABS', 'kurtosisABS', 'skewABS', 'label'])

# Create iterable list of all windows in TRAIN only
trainDict = {}
for key in HDF5File["dataset/Train"].keys():
    trainDict[key] = "Train"
trainKeys = list(trainDict.keys())

i = 0
for key in trainKeys:
    src = HDF5File["dataset/" + trainDict[key] + "/" + key]
    meanABS = pd.DataFrame(src).mean()[4]
    stdABS = pd.DataFrame(src).std()[4]
    maxABS = pd.DataFrame(src).max()[4]
    kurtosisABS = pd.DataFrame(src).kurt()[4]
    skewABS = pd.DataFrame(src).skew()[4]
    features_train.loc[i] = [meanABS] + [stdABS] + [maxABS] + [kurtosisABS] + [skewABS] + [src[0,5]]
    i += 1
features_train.to_csv("features_train.csv", index=False)

# SAME THING BUT FOR TEST SET

# Create iterable list of all windows in TEST only
testDict = {}
for key in HDF5File["dataset/Test"].keys():
    testDict[key] = "Test"
testKeys = list(testDict.keys())

i = 0
for key in testKeys:
    src = HDF5File["dataset/" + testDict[key] + "/" + key]
    meanABS = pd.DataFrame(src).mean()[4]
    stdABS = pd.DataFrame(src).std()[4]
    maxABS = pd.DataFrame(src).max()[4]
    kurtosisABS = pd.DataFrame(src).kurt()[4]
    skewABS = pd.DataFrame(src).skew()[4]
    features_test.loc[i] = [meanABS] + [stdABS] + [maxABS] + [kurtosisABS] + [skewABS] + [src[0,5]]
    i += 1
features_test.to_csv("features_test.csv", index=False)

print(features_train)
print(features_test)