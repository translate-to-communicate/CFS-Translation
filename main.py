# Updated 07JUN2023 10:04
import sys

from IPython.display import display

from tkinter import *
from tkinter import filedialog
from tkinter.filedialog import askdirectory

import pandas as pd
import numpy as np
import os
import glob
import ctypes
from PyQt5.QtCore import QTimer
from datetime import datetime, date

# The following code was used to enable all the data from a dataframe to be displayed in the run window (PyCharm)
# The code is a part of the pandas package
pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)
pd.set_option('display.width', None)
pd.set_option('display.max_colwidth', None)

time_milliseconds = 5000  # Setting the time to be used for auto closing windows (not used at the present)

# The goal is to bring in each individual file and store it as its own dataframe and not as a large dictionary as above

# Set the search path and the glob for the files
# Tk().withdraw()

# gui_win = Tk()
# gui_win.geometry('400x200')
# gui_win.grid_rowconfigure(0, weight=1)
# gui_win.grid_columnconfigure(0, weight=1)
#
#
#
# def directory():
#     ipath = filedialog.askdirectory(initialdir=r"C:/", title='Files Location')
#     label_path = Label(gui_win, text=ipath, font=('italic 14'))
#     label_path.pack(pady=20)
#
#
# dialog_btn = Button(gui_win, text='Select Directory', command=directory())
# dialog_btn.pack()
# gui_win.mainloop()

# root = Tk()
# root.directory = filedialog.askdirectory(initialdir="C:/", title="Files Location")
# print(root.directory)

ipath = Tk()
ipath.withdraw()
ipath.directory = filedialog.askdirectory(initialdir="C:/", title="Input Directory for CFS Files")
print(ipath.directory)

opath = Tk()
opath.withdraw()
opath.directory = filedialog.askdirectory(initialdir="C:/", title="Output Directory for CFS Translation Results")
print(opath)

print("Using glob.glob")
CSV_Files_CSV = glob.glob(ipath.directory + '/*')
# Show all the files that were identified
# for file in CSV_Files_CSV:
#   print(file)

# Make the system wait for user input to transition to the data processing
# input("The system is ready to start. Please press Enter to continue...")
# MessageBoxW = ctypes.windll.user32.MessageBoxW
# hWnd = None
# lpText = "Do you wish to start the program?"
# lpCaption = "CFS Start"
# uType = 0x40 | 0x1  # MB_ICONINFORMATION | MB_OKCANCEL

# result = MessageBoxW(hWnd, lpText, lpCaption, uType)

# if result == 1:  # User selects OK
#   QTimer.singleShot(time_milliseconds,
#                   lambda: ctypes.windll.user32.MessageBoxW(0, "Starting...", "Initiated", 0).done(0))

# QTimer.singleShot(time_milliseconds, lambda: CFS_Start_MSG.done(0))
# elif result == 2:  # User selected Cancel
#   ctypes.windll.user32.MessageBoxW(0, "Quitting...", "Halt", 0)
# quit()
# else:
#   print("??")

# ctypes.windll.user32.MessageBoxW(0, "The system is ready to start.", "Initiate", 1)

# result = MessageBoxW()


# The following code creates empty lists to store all the dataframes
li = []  # This list will be the unaltered dataframes
liz = []  # This list will be the altered dataframes

# The following code creates a list to store the column names that I want to see at the end
final_columns = ['agency', 'location', 'priority', 'call type', 'code', 'block address', 'area', 'merged location']

# Now we will loop through the list of files previously scanned, read each one into a dataframe, and append to the list
for f in CSV_Files_CSV:
    # Get the filename
    # print(f)
    agency = os.path.basename(f)
    print(f"Now processing: {agency}")
    # Read in the document
    if ".csv" in f:
        # print("This is a csv file")
        temp_df = pd.read_csv(f)
        # Create a new column with the file name for the agency at the leftmost portion of the dataframe
        temp_df.insert(0, 'Agency', agency)
        # data cleaning to remove the .csv
        temp_df['Agency'] = temp_df['Agency'].replace('.csv', '', regex=True)
        # Remove any underscores from the column headers
        temp_df = temp_df.rename(columns=lambda name: name.replace('_', ' '))
        # Create a new processed sheet for each agency
        # temp_df.to_csv(f"C:/Users/chris/Desktop/School Assignments/Summer/TEST OUTCOME/Processed_{agency}", index=False)
        temp_df.to_csv(f"{opath.directory}/Processed_{agency}", index=False)
        # add it to the list
        li.append(temp_df)
        # print(f'Successfully created dataframe for {agency} with shape {temp_df.shape}')
        temp_df.columns = map(str.lower, temp_df.columns)
        # print(temp_df.dtypes)
        # print(temp_df.columns)
        # This will merge location and block address columns
        if 'location' in temp_df.columns and 'block address' in temp_df.columns:
            # temp_df.insert(3, 'merged location', (temp_df['block address'] + ' : ' + temp_df['location']))
            print("Location data and block address data exists. Merging...")
            temp_df['merged location'] = temp_df['block address'] + ' ' + temp_df['location']
            # print(temp_df['merged location'])
        else:
            print('Location data and block address data DO NOT exist. Not merging')
        # Now we move on to the actual combination of files into one document
        temp_df = temp_df[temp_df.columns.intersection(final_columns)]
        liz.append(temp_df)
        # temp_df.to_csv(f"C:/Users/chris/Desktop/School Assignments/Summer/TEST OUTCOME/zz_{agency}", index=False)
        temp_df.to_csv(f"{opath.directory}/zz_{agency}", index=False)
        # print(temp_df.dtypes)
    elif ".xlsx" in f:
        # Run the same process as above but for Excel files
        temp_df = pd.read_excel(f)
        temp_df.insert(0, 'Agency', agency)
        temp_df['Agency'] = temp_df['Agency'].replace('.xlsx', '', regex=True)
        # temp_df.to_csv(f"C:/Users/chris/Desktop/School Assignments/Summer/TEST OUTCOME/Processed_{agency}.csv",
        #               index=False)
        temp_df.to_csv(f"{opath.directory}/Processed_{agency}.csv", index=False)
        li.append(temp_df)
        # print(f'Successfully created dataframe for {agency} with shape {temp_df.shape}')
        # Now we move on to the actual combination of files into one document
        temp_df.columns = map(str.lower, temp_df.columns)
        temp_df = temp_df[temp_df.columns.intersection(final_columns)]
        liz.append(temp_df)
        # temp_df.to_csv(f"C:/Users/chris/Desktop/School Assignments/Summer/TEST OUTCOME/zz_{agency}.csv", index=False)
        temp_df.to_csv(f"{opath.directory}/zz_{agency}.csv", index=False)
        # print(temp_df.dtypes)
    elif ".xml" in f:
        # Run the same process as above but for XML files
        temp_df = pd.read_xml(f)
        temp_df.insert(0, 'Agency', agency)
        temp_df['Agency'] = temp_df['Agency'].replace('.xml', '', regex=True)
        # temp_df.to_csv(f"C:/Users/chris/Desktop/School Assignments/Summer/TEST OUTCOME/Processed_{agency}.csv",
        #                index=False)
        temp_df.to_csv(f"{opath.directory}/Processed_{agency}.csv", index=False)
        li.append(temp_df)
        print(f'Successfully created dataframe for {agency} with shape {temp_df.shape}')
        # Now we move on to the actual combination of files into one document
        temp_df.columns = map(str.lower, temp_df.columns)
        temp_df = temp_df[temp_df.columns.intersection(final_columns)]
        liz.append(temp_df)
        # temp_df.to_csv(f"C:/Users/chris/Desktop/School Assignments/Summer/TEST OUTCOME/zz_{agency}.csv", index=False)
        temp_df.to_csv(f"{opath.directory}/zz_{agency}.csv", index=False)
        # print(temp_df.dtypes)
    else:
        # Display a message to indicate the file extension found is not able to be converted at this time
        # input(f"This file format is not available to be converted at this time: {agency}. Please press Enter to "
        # f"continue...")
        # USE THE ONE THAT FOLLOWS
        # ctypes.windll.user32.MessageBoxW(0, f"This file format is not available to be converted at this time: {agency}",
        #                                  "Extension Error", 1)
        print(f"The following file cannot be translated currently: {agency}")

# Now we will attempt to concatenate our list of dataframes into one
df = pd.concat(li, axis=0)
# print(f"The shape of the simple joined dataframe is: {df.shape}")
# df.head()

# Does above but for the data with the removed columns
df2 = pd.concat(liz, axis=0)
df2.reset_index(drop=True, inplace=True)

UID = "CR"  # This is the UID for the project
now = date.today()

# print(f"The shape of the modified and intersected dataframe is: {df2.shape}")
df2.index = df2.index.astype(str)
df2.index.name = 'UID'
df2.index = f"{UID}-{now}-" + df2.index
# print(df2.index)
# df.head()

# df.to_csv("C:/Users/chris/Desktop/School Assignments/Summer/TEST OUTCOME/SingleFile.csv")
# df2.to_csv("C:/Users/chris/Desktop/School Assignments/Summer/TEST OUTCOME/zzSingleFile.csv")
df.to_csv(f"{opath.directory}/SingleFile.csv")
df2.to_csv(f"{opath.directory}/zzSingleFile.csv")

# print(li)
# alldfs = [var for var in dir() if isinstance(eval(var), pd.core.frame.DataFrame)]
# print(temp_df)
# ctypes.windll.user32.MessageBoxW(0, "The process is complete", "Success", 1)

# The following is an attempt to allow the user to designate the folder holding the files
# Set the search path and the glob for the files
