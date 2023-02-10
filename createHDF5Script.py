import h5py as h5
import numpy as np

HDF5File = h5.File("data.hdf5", 'w')

# Level 1 Groups
HDF5File.create_group("Jillian")
HDF5File.create_group("Zack")
HDF5File.create_group("Zeerak")
HDF5File.create_group("dataset")

# Level 2 Groups
HDF5File["dataset"].create_group("Train")
HDF5File["dataset"].create_group("Test")

# Populate our groups with our data
for i in range(0,12):
   HDF5File["Jillian"].create_dataset(str(i)+"-Jillian", data=np.genfromtxt(".\\Data\\"+str(i)+"-Jillian\\"+str(i)+"-Jillian.csv", delimiter=',')[1:, :])
   HDF5File["Zack"].create_dataset(str(i)+"-Zack", data=np.genfromtxt(".\\Data\\"+str(i)+"-Zack\\"+str(i)+"-Zack.csv", delimiter=',')[1:, :])
   HDF5File["Zeerak"].create_dataset(str(i)+"-Zeerak", data=np.genfromtxt(".\\Data\\"+str(i)+"-Zeerak\\"+str(i)+"-Zeerak.csv", delimiter=',')[1:, :])


# Verification
print("Level 1 Groups: "+str(HDF5File.keys()))
print("Contents of Jillian: "+str(HDF5File["Jillian"].keys()))
print("Contents of Zack: "+str(HDF5File["Zack"].keys()))
print("Contents of Zeerak: "+str(HDF5File["Zeerak"].keys()))

print("Shape of \"4-Zack\": "+str(HDF5File["Zack"]["4-Zack"].shape))
