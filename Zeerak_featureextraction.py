import h5py as h5
import pandas as pd
import numpy as np

# Open file in read/write mode (we're going to apply SMA filter)
data = pd.read_csv("features_train.csv")
# features = pd.DataFrame(columns=['Mean', 'Min', 'Max', 'Median', 'Kurtosis', 'Skewness', 'STD'])
features_train = pd.DataFrame(columns=['meanABS', 'minABS', 'maxABS', 'medianABS', 'stdABS', 'kurtosisABS', 'skewABS', 'label', '', ''])
features_test = pd.DataFrame(columns=['meanABS', 'minABS', 'maxABS', 'medianABS', 'stdABS', 'kurtosisABS', 'skewABS', 'label', '', ''])

#print(features)