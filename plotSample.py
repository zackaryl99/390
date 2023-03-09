import pandas as pd
import matplotlib.pyplot as plot

headers = ['time', 'x-acceleration', 'y-acceleration', 'z-acceleration','absolute-acceleration']
data = pd.read_csv('/Data/0-Zeerak/0-Zeerak.csv', names=headers)

