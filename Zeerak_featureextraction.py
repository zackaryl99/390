import h5py as h5
import pandas as pd
import numpy as np

# Open file in read/write mode (we're going to apply SMA filter)
data = pd.read_csv("0-Zeerak.csv")
features = pd.DataFrame(data, columns=['Mean', 'Min', 'Max', 'Median', 'Kurtosis', 'Skewness', 'STD'])

#print(features)