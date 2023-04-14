#import numpy as np
import matplotlib.pyplot as plt
import seaborn as sb

#importing all the data for walk, jump and concatting them into one dataset
walk_data = pd.read_csv('new_data_walk.csv')
jump_data = pd.read_csv('new_data_jump.csv')
wj_data = pd.concat([walk_data, jump_data], keys = ['Walk', 'Jump'])

#Setting the heatmap data, and visulization setting
sb.set()
wj_data_hm = data.hm_table(index = 'Time (s)', columns = 'Team Member', values = ['Walking Acceleration', 'Jumping Acceleration'])
sb.heatmap(wj_data_hm, cmap='coolwarm')

#Setting the title, x-axis and y-axis label for the heat map
plt.title( "A 2D Heat Map of Walking vs. Jumping between All Members" )
plt.xlabel('Time and Condition')
plt.ylabel('Team Members')

#Plotting the heat map
plt.show()