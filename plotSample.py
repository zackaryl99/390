import pandas as pd
import matplotlib.pyplot as plot
import numpy as ny

headers = ['time', 'x-acceleration', 'y-acceleration', 'z-acceleration','absolute-acceleration']
data = pd.read_csv('Data/0-Zeerak/0-Zeerak.csv', names=headers)

plot.rcParams["figure.figsize"] = [7.5,3.5]
plot.rcParams["figure.autolayout"] = True

# data.set_index("x-acceleration").plot()
plot.plot(data.columns[1:4])
plot.xlabel('Time')
plot.ylabel('Acceleration')
plot.show()