import h5py as h5
import random
import pandas as pd
import matplotlib.pyplot as plt

random.seed()
HDF5File = h5.File("data.hdf5", 'r')

keyList = HDF5File["dataset/Train"].keys()
datasetsPandas = {}  # This will be a dictionary of the form {key : DataFrame}
for key in keyList:
   print(key)
   datasetsPandas[key] = pd.DataFrame(HDF5File["dataset/Train"][key])
print(datasetsPandas["11-Zack-Window5"][:][5])


# Compare walking between group mates
fig2, ax2 = plt.subplots()

ax2.plot(datasetsPandas["11-Zack-Window5"][:][0], datasetsPandas["11-Zack-Window5"][:][4])
ax2.set_title("Test")

plt.show()

