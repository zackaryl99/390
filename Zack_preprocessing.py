import h5py as h5
import pandas as pd
import matplotlib.pyplot as plt

# Open file in read/write mode (we're going to apply SMA filter)
HDF5File = h5.File("data.hdf5", 'r+')

# Create iterable list of all windows
allDatasetDict = {}
groupList = ["Train", "Test"]
for group in groupList:
    for key in HDF5File["dataset/" + group].keys():
        allDatasetDict[key] = group
allDatasetKeys = list(allDatasetDict.keys())

# For comparing on plot at end
orig = HDF5File["dataset/Train/train_69"][:] # make copy of dataset so we can apply "manual" sma later to verify script works

for key in allDatasetKeys: # Go through every 5-second window and apply SMA filter
   dataset = HDF5File["dataset/" + allDatasetDict[key]][key] # pointer to window in question
   dataset_sma = pd.DataFrame(dataset[:,1:]).rolling(20).mean() # create averaged version of aforementioned window
   dataset_sma = pd.concat([pd.DataFrame(dataset).iloc[:,0], dataset_sma], axis=1)
   dataset_sma.dropna(inplace=True) # drop all the NANs that the filter creates at beginning of dataset
   del HDF5File["dataset/" + str(allDatasetDict[key]) + "/" + str(key)] # delete old (unaveraged) window
   HDF5File["dataset/" + allDatasetDict[key]].create_dataset("sma_" + str(key), data=dataset_sma) # create new (averaged) window with same name, but "sma_" prefixed

# which column (acceleration) to plot
col = 2

# Compare walking between group mates
fig, ax = plt.subplots(2,2)

ax[0,0].plot(orig[:,0], orig[:,col])
ax[0,0].set_title('AUTOMATED (BEFORE)')

ax[1,0].plot(HDF5File["dataset/Train/sma_train_69"][:,0], HDF5File["dataset/Train/sma_train_69"][:,col])
ax[1,0].set_title('AUTOMATED (AFTER)')

ax[0,1].plot(orig[:,0], orig[:,col])
ax[0,1].set_title('MANUAL (BEFORE)')

manual = pd.DataFrame(orig).rolling(20).mean()

ax[1,1].plot(manual.iloc[:,0], manual.iloc[:,col])
ax[1,1].set_title('MANUAL (AFTER)')

fig.suptitle('Comparison before and after SMA filtering (wnd=20)', fontsize=16)
plt.tight_layout()
plt.show()
