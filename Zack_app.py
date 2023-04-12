import pandas as pd
import math
import matplotlib.pyplot as plt
import joblib
from sklearn.metrics import accuracy_score

# import trained model--------------------------------------------------------------------------------------------------
model = joblib.load("model.joblib")

# Read in supplied .csv (what we're trying to predict)------------------------------------------------------------------
new_data = pd.read_csv("new_data_walk.csv")

# Split into list of windows (~5 seconds long)--------------------------------------------------------------------------
winList = [] # List of 5-second windows (tables)
overlap = 5  # This is how much the window "jumps" forward each time. Increase for fewer windows
lines = new_data.shape[0]  # Number of lines in this dataset
start = 0  # Starting index always 0
end = int(math.floor(lines / 12))  # Guess of where first "end" will be (60seconds / 12 ~= 5 seconds)

while end < lines:  # While our window doesn't overflow EOF
    if new_data.iloc[end, 0] - new_data.iloc[start, 0] < 5:  # Increment window until it's JUST under 5 seconds long
        end += 1
        continue
    winList.append(new_data.iloc[start:end, :])  # Add this window to list of windows
    start += overlap
    end += overlap - 2  # This is so that we are under 5 seconds again, and iterate to find closest window to 5 seconds

# Apply SMA to each window (create new window list) --------------------------------------------------------------------
winListSMA = []
for win in winList:
    # filtered = win.rolling(20).mean()
    filtered = (win.iloc[:,1:]).rolling(5).mean()
    filtered = pd.concat([win.iloc[:,0], filtered], axis=1) # This is so we dont apply moving average filter to time col
    filtered.dropna(inplace=True)
    winListSMA.append(filtered)

# Extract features------------------------------------------------------------------------------------------------------
features = pd.DataFrame(columns=['meanABS', 'stdABS', 'maxABS', 'kurtosisABS', 'skewABS'])
i = 0
for win in winListSMA:
    meanABS = win.mean()[4]
    stdABS = win.std()[4]
    maxABS = win.max()[4]
    kurtosisABS = win.kurt()[4]
    skewABS = win.skew()[4]
    features.loc[i] = [meanABS] + [stdABS] + [maxABS] + [kurtosisABS] + [skewABS]
    i += 1

# Make predictions------------------------------------------------------------------------------------------------------
pred_test = model.predict(features)
print(pred_test)
print(len(pred_test))

# Collapse many overlapping windows into discrete (1-second) values-----------------------------------------------------
# To do this, create 60 discrete windows, then see which of the many windows overlap that one second
# Then compute the average in that 1-second interval (ex: 2 windows indicate jumping, 5 indicate walking =

discreteWin = []
for i in range(0, 60): # For each discrete time interval
    count = [0,0]
    corresponding = 0

    for win in winListSMA: # For each of the many windows
        if ((win.iloc[0, 0] >= i) and (win.iloc[0, 0] <= (i + 1))) or ((win.iloc[win.shape[0]-1, 0] >= i) and (win.iloc[win.shape[0]-1, 0] <= (i + 1))): # there is overlap
            count[int(pred_test[corresponding])] += 1
        corresponding += 1
    print(count[0] + count[1])
    if count[0] >= count[1]:
        discreteWin.append(0)
    else:
        discreteWin.append(1)

print(discreteWin)

# discreteWin = []
# for i in range(0, 60): # For each discrete time interval
#     value = 0.0
#     corresponding = 0
#     overlapCount = 0
#
#     for win in winListSMA: # For each of the many windows
#         if (win.iloc[0, 0] >= i) and (win.iloc[0, 0] <= (i + 1)):  # there is overlap
#             value += pred_test[corresponding] * (i + 1 - win.iloc[0, 0]) * 1.5
#             overlapCount += 1
#         elif (win.iloc[win.shape[0] - 1, 0] >= i) and (win.iloc[win.shape[0] - 1, 0] <= (i + 1)):
#             value += pred_test[corresponding] * (win.iloc[win.shape[0] - 1, 0]- i) * 1.5
#             overlapCount += 1
#         corresponding += 1
#     print(value)
#     print(overlapCount)
#     discreteWin.append(round(value/overlapCount))
#
# print(discreteWin)

# Plot predictions for each window--------------------------------------------------------------------------------------
fig, ax = plt.subplots()
ax.plot(range(0,len(pred_test)) ,pred_test)
ax.set_title('Predictions')
fig.suptitle('Predictions for windows of new (unseen) data', fontsize=16)

fig2, ax2 = plt.subplots()
ax2.plot(range(0,len(discreteWin)) ,discreteWin)
ax2.set_title('Predictions')
fig2.suptitle('Predictions for windows of new (unseen) data', fontsize=16)

plt.tight_layout()
plt.show()

# Export results in CSV-------------------------------------------------------------------------------------------------
