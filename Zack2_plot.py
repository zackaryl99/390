import matplotlib.pyplot as plt
import h5py as h5
HDF5File = h5.File("data.hdf5", 'r')
print(len(HDF5File["dataset/Train"].keys()))
# Compare walking vs jumping for Zack right-hand jacket procket
fig1, ax1 = plt.subplots(2,4)
for i in range(0,2):
    for j in range(0,4):
        ax1[i, j].set_ylim(-40, 40)
# WALKING
ax1[0, 0].plot(HDF5File["Zack"]["2-Zack"][:,0], HDF5File["Zack"]["2-Zack"][:,1])
ax1[0, 0].set_title('X Accel. [RHJ - Walking]')

ax1[0, 1].plot(HDF5File["Zack"]["2-Zack"][:,0], HDF5File["Zack"]["2-Zack"][:,2])
ax1[0, 1].set_title('Y Accel. [RHJ - Walking]')

ax1[1, 0].plot(HDF5File["Zack"]["2-Zack"][:,0], HDF5File["Zack"]["2-Zack"][:,3])
ax1[1, 0].set_title('Z Accel. [RHJ - Walking]')

ax1[1, 1].plot(HDF5File["Zack"]["2-Zack"][:,0], HDF5File["Zack"]["2-Zack"][:,4])
ax1[1, 1].set_title('Abs. Accel. [RHJ - Walking]')

# JUMPING
ax1[0, 2].plot(HDF5File["Zack"]["8-Zack"][:,0], HDF5File["Zack"]["8-Zack"][:,1])
ax1[0, 2].set_title('X Accel. [RHJ - Jumping]')

ax1[0, 3].plot(HDF5File["Zack"]["8-Zack"][:,0], HDF5File["Zack"]["8-Zack"][:,2])
ax1[0, 3].set_title('Y Accel. [RHJ - Jumping]')

ax1[1, 2].plot(HDF5File["Zack"]["8-Zack"][:,0], HDF5File["Zack"]["8-Zack"][:,3])
ax1[1, 2].set_title('Z Accel. [RHJ - Jumping]')

ax1[1, 3].plot(HDF5File["Zack"]["8-Zack"][:,0], HDF5File["Zack"]["8-Zack"][:,4])
ax1[1, 3].set_title('Abs. Accel. [RHJ - Jumping]')

fig1.suptitle('Comparison of walking vs jumping', fontsize=16)

# Compare walking between group mates
fig2, ax2 = plt.subplots(1,3)
for j in range(0,3):
    ax2[j].set_ylim(-40, 40)
    ax2[j].set_xlim(0, 60)

ax2[0].plot(HDF5File["Jillian"]["2-Jillian"][:,0], HDF5File["Jillian"]["2-Jillian"][:,4])
ax2[0].set_title('Jillian')

ax2[1].plot(HDF5File["Zack"]["2-Zack"][:,0], HDF5File["Zack"]["2-Zack"][:,4])
ax2[1].set_title('Zack')

ax2[2].plot(HDF5File["Zeerak"]["2-Zeerak"][:,0], HDF5File["Zeerak"]["2-Zeerak"][:,4])
ax2[2].set_title('Zeerak')

fig2.suptitle('Comparison of Abs. Accel. while jumping in right jacket pocket', fontsize=16)

# Compare walking between group mates
fig3, ax3 = plt.subplots(2,3)

#for walking
for j in range(0,3):
    ax3[0,j].set_ylim(-40, 40)
    ax3[0,j].set_xlim(0, 60)

#for jumping
for j in range(0,3):
    ax3[1,j].set_ylim(-10, 70)
    ax3[1,j].set_xlim(0, 60)
# WALKING
ax3[0,0].plot(HDF5File["Jillian"]["2-Jillian"][:,0], HDF5File["Jillian"]["2-Jillian"][:,4])
ax3[0,0].set_title('Jillian [walking]')

ax3[0,1].plot(HDF5File["Zack"]["2-Zack"][:,0], HDF5File["Zack"]["2-Zack"][:,4])
ax3[0,1].set_title('Zack [walking]')

ax3[0,2].plot(HDF5File["Zeerak"]["2-Zeerak"][:,0], HDF5File["Zeerak"]["2-Zeerak"][:,4])
ax3[0,2].set_title('Zeerak [walking]')

# JUMPING
ax3[1,0].plot(HDF5File["Jillian"]["8-Jillian"][:,0], HDF5File["Jillian"]["8-Jillian"][:,4])
ax3[1,0].set_title('Jillian [jumping]')

ax3[1,1].plot(HDF5File["Zack"]["8-Zack"][:,0], HDF5File["Zack"]["8-Zack"][:,4])
ax3[1,1].set_title('Zack [jumping]')

ax3[1,2].plot(HDF5File["Zeerak"]["8-Zeerak"][:,0], HDF5File["Zeerak"]["8-Zeerak"][:,4])
ax3[1,2].set_title('Zeerak [jumping]')

fig3.suptitle('Comparison of walking vs jumping', fontsize=16)


plt.tight_layout()
plt.show()