import h5py as h5
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.pipeline import make_pipeline
from sklearn.linear_model import LogisticRegression
from sklearn.decomposition import PCA
import joblib


# Create HDF5 file (root)
HDF5File = h5.File("data.hdf5", 'r')

# Read features into dataframe
features_train = pd.read_csv("features_train.csv")
features_test = pd.read_csv("features_test.csv")

# Split training into data (features) and labels (1/0)
data_train = features_train.iloc[:,0:-1]
labels_train = features_train.iloc[:,-1]

# Split testing into data (features) and labels (1/0)
data_test = features_test.iloc[:,0:-1]
labels_test = features_test.iloc[:,-1]

# normalizer
scaler = StandardScaler()

# Logistic regression and classifier
l_reg = LogisticRegression(max_iter=100000)
clf = make_pipeline(scaler, l_reg)

# Train the classifier with data and labels
clf.fit(data_train, labels_train)

# Generate predictions for all test data
pred_test = clf.predict(data_test)

# Gauge accuracy of above predictions
print(accuracy_score(labels_test, pred_test))

# Save trained model (this will be used by APP so it doesn't have to re-train every time)
joblib.dump(clf, "model.joblib")




