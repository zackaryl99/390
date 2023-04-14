import h5py as h5
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split

# Create HDF5 file (root)
HDF5File = h5.File("data.hdf5", 'r')

# Create iterable list of all windows in TRAIN only
trainDict = {}
for key in HDF5File["dataset/Train"].keys():
    trainDict[key] = "Train"
trainKeys = list(trainDict.keys())

# Create iterable list of all windows in TEST only
testDict = {}
for key in HDF5File["dataset/Test"].keys():
    testDict[key] = "Test"
testKeys = list(testDict.keys())

# The set of features used for training was varied to find the optimal set. Change this parameter to see differing results
featureSet = 'C'

# Three different cases of which features to write, based on which feature-set to experiment with.
if featureSet == 'A':
    features_train = pd.DataFrame(columns=['meanX', 'meanY', 'meanZ', 'stdX', 'stdY', 'stdZ', 'maxX', 'maxY', 'maxZ', 'kurtosisX', 'kurtosisY', 'kurtosisZ', 'skewX', 'skewY', 'skewZ', 'label'])
    features_test = pd.DataFrame(columns=['meanX', 'meanY', 'meanZ', 'stdX', 'stdY', 'stdZ', 'maxX', 'maxY', 'maxZ', 'kurtosisX', 'kurtosisY', 'kurtosisZ', 'skewX', 'skewY', 'skewZ', 'label'])
    i = 0
    for key in trainKeys:
        src = HDF5File["dataset/" + trainDict[key] + "/" + key]

        meanX = pd.DataFrame(src).mean()[1]
        meanY = pd.DataFrame(src).mean()[2]
        meanZ = pd.DataFrame(src).mean()[3]

        stdX = pd.DataFrame(src).std()[1]
        stdY = pd.DataFrame(src).std()[2]
        stdZ = pd.DataFrame(src).std()[3]

        maxX = pd.DataFrame(src).max()[1]
        maxY = pd.DataFrame(src).max()[2]
        maxZ = pd.DataFrame(src).max()[3]

        kurtosisX = pd.DataFrame(src).kurt()[1]
        kurtosisY = pd.DataFrame(src).kurt()[2]
        kurtosisZ = pd.DataFrame(src).kurt()[3]

        skewX = pd.DataFrame(src).skew()[1]
        skewY = pd.DataFrame(src).skew()[2]
        skewZ = pd.DataFrame(src).skew()[3]

        features_train.loc[i] = [meanX] + [meanY] + [meanZ] + [stdX] + [stdY] + [stdZ] + [maxX] + [maxY] + [maxZ] + [kurtosisX] + [kurtosisY] + [kurtosisZ] + [skewX] + [skewY] + [skewZ] + [src[0, 5]]
        i += 1

    i = 0
    for key in testKeys:
        src = HDF5File["dataset/" + testDict[key] + "/" + key]
        meanX = pd.DataFrame(src).mean()[1]
        meanY = pd.DataFrame(src).mean()[2]
        meanZ = pd.DataFrame(src).mean()[3]

        stdX = pd.DataFrame(src).std()[1]
        stdY = pd.DataFrame(src).std()[2]
        stdZ = pd.DataFrame(src).std()[3]

        maxX = pd.DataFrame(src).max()[1]
        maxY = pd.DataFrame(src).max()[2]
        maxZ = pd.DataFrame(src).max()[3]

        kurtosisX = pd.DataFrame(src).kurt()[1]
        kurtosisY = pd.DataFrame(src).kurt()[2]
        kurtosisZ = pd.DataFrame(src).kurt()[3]

        skewX = pd.DataFrame(src).skew()[1]
        skewY = pd.DataFrame(src).skew()[2]
        skewZ = pd.DataFrame(src).skew()[3]

        features_test.loc[i] = [meanX] + [meanY] + [meanZ] + [stdX] + [stdY] + [stdZ] + [maxX] + [maxY] + [maxZ] + [kurtosisX] + [kurtosisY] + [kurtosisZ] + [skewX] + [skewY] + [skewZ] + [src[0, 5]]
        i += 1

elif featureSet == 'B':
    features_train = pd.DataFrame(columns=['meanABS', 'stdABS', 'maxABS', 'kurtosisABS', 'skewABS', 'label'])
    features_test = pd.DataFrame(columns=['meanABS', 'stdABS', 'maxABS', 'kurtosisABS', 'skewABS', 'label'])

    i = 0
    for key in trainKeys:
        src = HDF5File["dataset/" + trainDict[key] + "/" + key]
        meanABS = pd.DataFrame(src).mean()[4]
        stdABS = pd.DataFrame(src).std()[4]
        maxABS = pd.DataFrame(src).max()[4]
        kurtosisABS = pd.DataFrame(src).kurt()[4]
        skewABS = pd.DataFrame(src).skew()[4]
        features_train.loc[i] = [meanABS] + [stdABS] + [maxABS] + [kurtosisABS] + [skewABS] + [src[0, 5]]
        i += 1

    i = 0
    for key in testKeys:
        src = HDF5File["dataset/" + testDict[key] + "/" + key]
        meanABS = pd.DataFrame(src).mean()[4]
        stdABS = pd.DataFrame(src).std()[4]
        maxABS = pd.DataFrame(src).max()[4]
        kurtosisABS = pd.DataFrame(src).kurt()[4]
        skewABS = pd.DataFrame(src).skew()[4]
        features_test.loc[i] = [meanABS] + [stdABS] + [maxABS] + [kurtosisABS] + [skewABS] + [src[0, 5]]
        i += 1

elif featureSet == 'C':
    features_train = pd.DataFrame(columns=['meanX', 'meanY', 'meanZ', 'maxX', 'maxY', 'maxZ', 'minX', 'minY', 'minZ', 'kurtosisX', 'kurtosisY', 'kurtosisZ', 'rangeX', 'rangeY', 'rangeZ', 'varianceX', 'varianceY', 'varianceZ', 'label'])
    features_test = pd.DataFrame(columns=['meanX', 'meanY', 'meanZ', 'maxX', 'maxY', 'maxZ', 'minX', 'minY', 'minZ', 'kurtosisX', 'kurtosisY', 'kurtosisZ', 'rangeX', 'rangeY', 'rangeZ', 'varianceX', 'varianceY', 'varianceZ', 'label'])
    i = 0
    for key in trainKeys:
        src = HDF5File["dataset/" + trainDict[key] + "/" + key]

        meanX = pd.DataFrame(src).mean()[1]
        meanY = pd.DataFrame(src).mean()[2]
        meanZ = pd.DataFrame(src).mean()[3]

        maxX = pd.DataFrame(src).max()[1]
        maxY = pd.DataFrame(src).max()[2]
        maxZ = pd.DataFrame(src).max()[3]

        minX = pd.DataFrame(src).min()[1]
        minY = pd.DataFrame(src).min()[2]
        minZ = pd.DataFrame(src).min()[3]
        
        kurtosisX = pd.DataFrame(src).kurt()[1]
        kurtosisY = pd.DataFrame(src).kurt()[2]
        kurtosisZ = pd.DataFrame(src).kurt()[3]

        # Range

        varianceX = pd.DataFrame(src).var()[1]
        varianceY = pd.DataFrame(src).var()[2]
        varianceZ = pd.DataFrame(src).var()[3]

        features_train.loc[i] = [meanX] + [meanY] + [meanZ] + [maxX] + [maxY] + [maxZ] + [minX] + [minY] + [minZ] + [kurtosisX] + [kurtosisY] + [kurtosisZ] + [maxX-minX] + [maxY-minY] + [maxZ-minZ] + [varianceX] + [varianceY] + [varianceZ] + [src[0, 5]]
        i += 1

    i = 0
    for key in testKeys:
        src = HDF5File["dataset/" + testDict[key] + "/" + key]
        meanX = pd.DataFrame(src).mean()[1]
        meanY = pd.DataFrame(src).mean()[2]
        meanZ = pd.DataFrame(src).mean()[3]

        maxX = pd.DataFrame(src).max()[1]
        maxY = pd.DataFrame(src).max()[2]
        maxZ = pd.DataFrame(src).max()[3]

        minX = pd.DataFrame(src).min()[1]
        minY = pd.DataFrame(src).min()[2]
        minZ = pd.DataFrame(src).min()[3]

        kurtosisX = pd.DataFrame(src).kurt()[1]
        kurtosisY = pd.DataFrame(src).kurt()[2]
        kurtosisZ = pd.DataFrame(src).kurt()[3]

        # Range

        varianceX = pd.DataFrame(src).var()[1]
        varianceY = pd.DataFrame(src).var()[2]
        varianceZ = pd.DataFrame(src).var()[3]

        features_test.loc[i] = [meanX] + [meanY] + [meanZ] + [maxX] + [maxY] + [maxZ] + [minX] + [minY] + [minZ] + [kurtosisX] + [kurtosisY] + [kurtosisZ] + [maxX-minX] + [maxY-minY] + [maxZ-minZ] + [varianceX] + [varianceY] + [varianceZ] + [src[0, 5]]
        i += 1


features_train.to_csv("features_train.csv", index=False)
features_test.to_csv("features_test.csv", index=False)
