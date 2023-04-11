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

# import trained model
model = joblib.load("model.joblib")

# Read in supplied .csv (what we're trying to predict)

# Split into windows

# Apply SMA

# Extract features

# Make predictions

# Plot predictions for each window
model.predict()