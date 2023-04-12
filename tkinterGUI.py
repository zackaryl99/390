import pandas as pd
import tkinter as tk
from tkinter import *
from tkinter import ttk
from tkinter import filedialog
import matplotlib.pyplot as plt
import h5py as h5
import joblib
import math
HDF5File = h5.File("data.hdf5", 'r')
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,
                                               NavigationToolbar2Tk)
# Initializing window and window size
my_w = tk.Tk()
my_w.geometry("1000x700")  # Size of the window
my_w.title('www.csvclassifier.com')

# Add image file
bg = PhotoImage(file="orange.png")

# Variable to hold filepath of selected CSV
filepath = ""

# Create a frame widget
#frame=Frame(my_w, width=300, height=300)
#frame.grid(row=0, column=0, sticky="NW")

# Create a label widget
label=Label(my_w, text="I am inside a Frame", font='Arial 17 bold')
label.place(relx=0.5, rely=0.5, anchor=CENTER)

# Show image using label
label1 = Label(my_w, image=bg)
label1.place(x=0, y=0)

#Initializing text
my_font1 = ('times', 12, 'bold')
my_font2 = ('times', 20, 'bold')

#Adding space on left
label.grid(row=1, column=1, padx=5)

label = tk.Label(
    text="Welcome to our CSV Classifier",
    fg="white",
    bg="black",
    width=40,
    height=3,
    font=my_font2
)
label.grid(row=1, column=2, padx=5)

lb1 = tk.Label(my_w, text='Read File & create DataFrame',
               width=30, font=my_font1)
lb1.grid(row=2, column=2, pady=5)
b1 = tk.Button(my_w, text='Browse File',
               width=20, command=lambda: upload_file_wrapper())
b1.grid(row=3, column=2, pady=5)
lb2 = tk.Label(my_w, width=40, text='', bg='lightyellow')
lb2.grid(row=4, column=2, padx=5)
l1 = []  # List to hold headers of the Treeview

def upload_file_wrapper():
    global filepath
    filepath = upload_file()

def upload_file():
    global df, l1
    f_types = [('CSV files', "*.csv"), ('All', "*.*")]
    file = filedialog.askopenfilename(filetypes=f_types)
    print(file)
    lb1.config(text=file)  # display the path
    df = pd.read_csv(file)  # create DataFrame
    l1 = list(df)  # List of column names as header
    str1 = "Rows:" + str(df.shape[0]) + " , Columns:" + str(df.shape[1])
    # print(str1)
    lb2.config(text=str1)  # add to Text widget
    trv_refresh()  # show Treeview
    return file

def trv_refresh():  # Refresh the Treeview to reflect changes
    global df, trv, l1
    r_set = df.to_numpy().tolist()  # create list of list using rows
    trv = ttk.Treeview(my_w, selectmode='browse', height=10,
                       show='headings', columns=l1)
    trv.grid(row=5, column=2, columnspan=3, padx=10, pady=20)

    for i in l1:
        trv.column(i, width=90, anchor='c')
        trv.heading(i, text=str(i))
    for dt in r_set:
        v = [r for r in dt]
        trv.insert("", 'end', iid=v[0], values=v)


def classify():
    # import trained model----------------------------------------------------------------------------------------------
    model = joblib.load("model.joblib")

    # Read in supplied .csv (what we're trying to predict)--------------------------------------------------------------
    new_data = pd.read_csv(filepath)

    # Split into list of windows (~5 seconds long)----------------------------------------------------------------------
    winList = []  # List of 5-second windows (tables)
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
        end += overlap - 2  # This is so that we are under 5 seconds again, and iterate to find closest window to 5 secs

    # Apply SMA to each window (create new window list) ----------------------------------------------------------------
    winListSMA = []
    for win in winList:
        # filtered = win.rolling(20).mean()
        filtered = (win.iloc[:, 1:]).rolling(5).mean()
        filtered = pd.concat([win.iloc[:, 0], filtered],
                             axis=1)  # This is so we dont apply moving average filter to time col
        filtered.dropna(inplace=True)
        winListSMA.append(filtered)

    # Extract features--------------------------------------------------------------------------------------------------
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

    # Make predictions--------------------------------------------------------------------------------------------------
    pred_test = model.predict(features)
    print(pred_test)

    # Plot predictions for each window----------------------------------------------------------------------------------
    fig, ax = plt.subplots()
    ax.plot(range(0, len(pred_test)), pred_test)
    ax.set_title('Predictions')
    fig.suptitle('Predictions for windows of new (unseen) data', fontsize=16)
    canvas = FigureCanvasTkAgg(fig, master=my_w)
    canvas.draw()

    # placing the canvas on the Tkinter window
    canvas.get_tk_widget().grid(row=6, column=2, pady=5, padx=5)

    # placing the toolbar on the Tkinter window
    canvas.get_tk_widget().grid()

    #write results to csv
    results = pd.DataFrame(data=pred_test)
    results.to_csv("results.csv")


# button that displays the plot

b2 = tk.Button(my_w, text='Plot',
               width=20, bg='red', command=lambda: classify())
b2.grid(row=10, column=2, padx=5)
# place the button
# in main window


my_w.mainloop()  # Keep the window open
