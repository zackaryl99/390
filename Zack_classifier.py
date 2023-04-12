import h5py as h5
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split

from sklearn.metrics import accuracy_score
from sklearn.metrics import recall_score
from sklearn.metrics import roc_auc_score
from sklearn.metrics import f1_score
from sklearn.metrics import roc_curve
from sklearn.metrics import confusion_matrix
from sklearn.metrics import ConfusionMatrixDisplay
from sklearn.metrics import RocCurveDisplay


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
pred_prob_test = clf.predict_proba(data_test)

# performance metrics
print("Accuracy: " + str(accuracy_score(labels_test, pred_test)))
print("Recall: " + str(recall_score(labels_test, pred_test)))
print("AUC: " + str(roc_auc_score(labels_test, pred_prob_test[:, 1])))
print("F1: " + str(f1_score(labels_test, pred_test)))

cm = confusion_matrix(labels_test, pred_test)
cm_display = ConfusionMatrixDisplay(cm).plot()

fpr, tpr, _ = roc_curve(labels_test, pred_prob_test[:, 1], pos_label=clf.classes_[1])
roc_display = RocCurveDisplay(fpr=fpr, tpr=tpr).plot()

plt.show()

# Save trained model (this will be used by APP so it doesn't have to re-train every time)
joblib.dump(clf, "model.joblib")




