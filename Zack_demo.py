import h5py as h5
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button
import math

def y(i):
    return dataset1[int(i)*wS[1]:(int(i)+1)*wS[1],4]

def update(val):
    line.set_ydata(y(freq_slider.val))
    fig.canvas.draw_idle()

# Open HDF5
HDF5File = h5.File("data.hdf5", 'r')

keyList = list([key for key in HDF5File["dataset/Train"].keys()])
dataset0 = HDF5File["Jillian"]["0-Jillian"]  # Walking
dataset1 = HDF5File["Jillian"]["6-Jillian"]  # Jumping

wS = [int(math.floor(dataset0.shape[0]/12)), int(math.floor(dataset1.shape[0]/12))]  # Window size (~5s)
i = 4

fig, ax = plt.subplots(2,2)
line, = ax[0,0].plot(dataset0[:,0], dataset0[:,4])
line, = ax[0,1].plot(dataset1[:,0], dataset1[:,4])

line, = ax[1,0].plot(dataset0[2*wS[0]:(2+1)*wS[0],0], dataset0[2*wS[0]:(2+1)*wS[0],4])
line, = ax[1,1].plot(dataset1[4*wS[1]:(4+1)*wS[1],0], dataset1[2*wS[1]:(2+1)*wS[1],4])
fig.suptitle('Plot of ' + str(keyList[6]), fontsize=16)




axfreq = fig.add_axes([0.25, 0.1, 0.65, 0.03])
freq_slider = Slider(
    ax=axfreq,
    label='i',
    valmin=0,
    valmax=11,
    valinit=5,
)

freq_slider.on_changed(update)

plt.show()

