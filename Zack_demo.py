import h5py as h5
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.widgets import Slider, Button
import math

def y0(i):
    return dataset0[int(i*w):int((i+1)*w),4]

def y1(i):
    return dataset1[int(i*w):int((i+1)*w),4]

def update(val):
    line.set_ydata(y0(slider.val))
    line2.set_ydata(y1(slider.val))
    marker.set_xdata(30 + (val-5.5)*(30/5.5))
    marker2.set_xdata(30 + (val - 5.5) * (30 / 5.5))
    print(str((val*w)*s) + "s to " + str(((1+val)*w)*s) + "s")
    fig.canvas.draw_idle()

# Open HDF5
HDF5File = h5.File("data.hdf5", 'r')

keyList = list([key for key in HDF5File["dataset/Train"].keys()])
dataset0 = HDF5File["Jillian"]["0-Jillian"]  # Walking
dataset1 = HDF5File["Jillian"]["8-Jillian"]  # jumping

w = int(dataset0.shape[0]/12)
s = 60/dataset0.shape[0]

fig, ax = plt.subplots(2,2)

for j in range(0,2):
    ax[0,j].set_ylim(-5, 70)
    ax[0,j].set_xlim(0, 60)

for j in range(0,2):
    ax[1,j].set_ylim(-5, 70)

ax[0,0].plot(dataset0[:,0], dataset0[:,4])
ax[0,1].plot(dataset1[:,0], dataset1[:,4])

line, = ax[1,0].plot(dataset0[5*w:6*w,0], dataset0[5*w:6*w,4])
line2, = ax[1,1].plot(dataset1[5*w:6*w,0], dataset1[5*w:6*w,4])
fig.suptitle('Comparaison of walking and jumping, sliding window' + str(keyList[6]), fontsize=16)

[marker] = ax[0,0].plot((30,30), (-5,70), scaley = False)
[marker2] = ax[0,1].plot((30,30), (-5,70), scaley = False)



axslider = fig.add_axes([0.175, 0.1, 0.65, 0.02])
slider = Slider(
    ax=axslider,
    label='i',
    valmin=0,
    valmax=11,
    valinit=5.5,
)

slider.on_changed(update)
fig.subplots_adjust(bottom=0.25)
plt.show()

