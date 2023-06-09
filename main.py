# Updated 08JUN2023 13:25
# Author: Christopher Romeo
# This is the working branch for naming the input files using a prompt for the user
# The script now prompts the user to identify the responsible agency for each file
import sys
from IPython.display import display
import tkinter as tk
from PyQt5 import QtGui, QtCore
import tkinter.ttk as ttk
from tkinter import *
from tkinter.simpledialog import askstring
from tkinter.messagebox import showinfo
from tkinter import ttk
import tkinter.messagebox as mbox
from tkinter import filedialog
from tkinter.filedialog import askdirectory
import pandas as pd
from tabulate import tabulate
import numpy as np
import os
import glob
import ctypes
from PyQt5.QtCore import QTimer
from datetime import datetime, date


# def get_curr_screen_geometry():
#     """
#         Workaround to get the size of the current screen in a multi-screen setup.
#
#         Returns:
#             geometry (str): The standard Tk geometry string.
#                 [width]x[height]+[left]+[top]
#         """
#     root = tk.Tk()
#     root.update_idletasks()
#     root.attributes('-fullscreen', True)
#     root.state('iconic')
#     geometry = root.winfo_geometry()
#     root.destroy()
#     return geometry

# This is the function that determines if the user wants to keep or delete the column
# It shows the first line of data from that column (can be problematic if there are blanks sporadically)
# Running a loop before sending the df information to the function may help solve a blank field by running through
# the rows until a non-null value is found
def call(col, df):
    twin = tk.Tk()
    twin.withdraw()
    yes_to_keep = col
    no_to_keep = 'Deleted'
    example = df
    result = mbox.askyesno('Column Selection', f"Do you want keep the following column: {col}?"
                                               f" An example of the data hosted in this column is: {example}")
    if result:
        twin.destroy()
        return yes_to_keep
    else:
        twin.destroy()
        return no_to_keep


def main():
    # The following code was used to enable all the data from a dataframe to be displayed in the run window (PyCharm)
    # The code is a part of the pandas package
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    time_milliseconds = 5000  # Setting the time to be used for auto closing windows (not used at the present)

    # Open the file explorer to allow the user to select both the input and output directories
    # ipath is the input directory path and opath is the output directory path
    # There will be two versions of this directory information to allow for faster testing

    # ipath = Tk()
    # ipath.withdraw()
    # ipath.directory = filedialog.askdirectory(initialdir="C:/", title="Input Directory for CFS Files")
    # print('The chosen input directory is: ' + ipath.directory)
    #
    # opath = Tk()
    # opath.withdraw()
    # opath.directory = filedialog.askdirectory(initialdir="C:/", title="Output Directory for CFS Translation Results")
    # print('The chosen output directory is: ' + opath.directory)

    ipath = "C:/Users/chris/Desktop/School Assignments/Summer/TEST DATA"
    opath = "C:/Users/chris/Desktop/School Assignments/Summer/TEST OUTCOME"

    # This pulls all files in the chosen directory
    print("Using glob.glob")
    # csv_files_csv = glob.glob(ipath.directory + '/*')  # This is the production code
    csv_files_csv = glob.glob(ipath + '/*')  # This is the quick testing code

    # Show all the files that were identified
    # for file in csv_files_csv:
    #   print(file)

    # The following code creates empty lists to store all the dataframes
    li = []  # This list will be the unaltered dataframes
    liz = []  # This list will be the altered dataframes

    # The following code creates a list to store the column names that I want to see at the end
    final_columns = ['agency', 'location', 'priority', 'call type', 'code', 'block address', 'area', 'merged location']

    # Call the screen resolution function
    # print(get_curr_screen_geometry())

    # The goal is to bring in each individual file and store it as its own dataframe and not as a large dictionary
    # Here we loop through the list of files previously scanned, read each one into a dataframe, and append to the list
    for f in csv_files_csv:
        # Get the filename
        # print(f)
        agency = os.path.basename(f)
        print(f"Now processing: {agency}")

        # # Generate the user prompt to ensure proper agency information
        # win = tk.Tk()
        # win.title('Agency Selection')
        # win.geometry("")
        #
        # leb = ttk.Label(win, text=f'What is the responsible agency for the file: {agency}')
        # leb.grid(row=0, column=0)
        #
        # entb = ttk.Entry(win)
        # entb.grid(row=0, column=1, columnspan=2)
        #
        # def show():
        #     mbox.showinfo('Agency', f'{entb}')
        #
        # btn = ttk.Button(win, text='Show', command=show)
        # btn.grid(row=1, column=1)
        # # Also if you want to destroy your GUI it is better to use 'win.destroy()' instead of 'exit()'
        # btn1 = ttk.Button(win, text='Exit', command=win.destroy)
        # btn1.grid(row=1, column=2)
        #
        # win.mainloop()
        #
        #
        # This is the code that was working with the pop-up input boxes                                             #
        #                                                                                                           #
        win = tk.Tk()
        # win.geometry(get_curr_screen_geometry())  # Makes a fullscreen window
        win.geometry("")
        win.withdraw()  # Hides the tk window
        enta = askstring('Agency', f'What is the responsible agency for the file: {agency}?')
        win.destroy()  # Ensures the window is closed for performance purposes
        # # # This loop ensures that if the user does not input any information, hits cancel, or the 'x' that the   #
        # # # agency information does not change and cause an error. This will default to the file basename.        #
        if enta == '':
            print(f'No input given for: {agency}')
        elif enta is None:
            print(f"No input given for: {agency}")
        else:
            agency = enta
        # # showinfo('Agency', f'The responsible agency is: {enta}')
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
            # temp_df.to_csv(f"{opath.directory}/Processed_{agency}", index=False)  # This is the production code
            temp_df.to_csv(f"{opath}/Processed_{agency}.csv", index=False)  # This is the one for quick testing only
            # add it to the list
            li.append(temp_df)
            #                                                                                                       #
            # This is the working space to identify the number of columns per dataframe / file that is processed.   #
            # The goal will be to create a loop that presents the user with the columns and the first row of data   #
            # So that the user can identify which columns are to be saved / merged onto the final document.         #
            #                                                                                                       #
            # numcolumns = len(temp_df.columns)  # The attempt here was to create a variable with the number of
            # print(numcolumns)  # columns used and then run a loop. Doesn't appear necessary now as the built in
            # for(columnName) in temp_df.columns:  # columnName inside a for loop works just as well.
            #     print(columnName)
            # print(f'Successfully created dataframe for {agency} with shape {temp_df.shape}')
            #
            # Here I want to ask the user what columns they wish to keep
            for col in temp_df:
                colb = col
                example = temp_df[col].iloc[0]
                result = call(colb, example)
                # print(call(colb, example))
                print(result)
                # col_lab = ttk.Label(win_col, text=f'Do you want to keep the following column: {col}?')
                # col_lab.grid(row=0, column=0)
                #
                # col_ent = ttk.Entry(win_col)
                # col_ent.grid(row=0, column=1, columnspan=2)
            #
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
            # temp_df.to_csv(f"{opath.directory}/zz_{agency}", index=False)  # This is the production code
            temp_df.to_csv(f"{opath}/zz_{agency}.csv", index=False)  # This is the one for quick testing only
            # print(temp_df.dtypes)
        elif ".xlsx" in f:
            # Run the same process as above but for Excel files
            temp_df = pd.read_excel(f)
            temp_df.insert(0, 'Agency', agency)
            temp_df['Agency'] = temp_df['Agency'].replace('.xlsx', '', regex=True)
            # temp_df.to_csv(f"{opath.directory}/Processed_{agency}.csv", index=False)  # This is the production code
            temp_df.to_csv(f"{opath}/Processed_{agency}.csv", index=False)  # This is the one for quick testing only
            li.append(temp_df)
            # print(f'Successfully created dataframe for {agency} with shape {temp_df.shape}')
            # Now we move on to the actual combination of files into one document
            temp_df.columns = map(str.lower, temp_df.columns)
            temp_df = temp_df[temp_df.columns.intersection(final_columns)]
            liz.append(temp_df)
            # temp_df.to_csv(f"{opath.directory}/zz_{agency}.csv", index=False)  # This is the production code
            temp_df.to_csv(f"{opath}/zz_{agency}.csv", index=False)  # This is the one for quick testing only
            # print(temp_df.dtypes)
        elif ".xml" in f:
            # Run the same process as above but for XML files
            temp_df = pd.read_xml(f)
            temp_df.insert(0, 'Agency', agency)
            temp_df['Agency'] = temp_df['Agency'].replace('.xml', '', regex=True)
            # temp_df.to_csv(f"{opath.directory}/Processed_{agency}.csv", index=False)  # This is the production code
            temp_df.to_csv(f"{opath}/Processed_{agency}.csv", index=False)  # This is the one for quick testing only
            li.append(temp_df)
            print(f'Successfully created dataframe for {agency} with shape {temp_df.shape}')
            # Now we move on to the actual combination of files into one document
            temp_df.columns = map(str.lower, temp_df.columns)
            temp_df = temp_df[temp_df.columns.intersection(final_columns)]
            liz.append(temp_df)
            # temp_df.to_csv(f"{opath.directory}/zz_{agency}.csv", index=False)  # This is the production code
            temp_df.to_csv(f"{opath}/zz_{agency}.csv", index=False)  # This is the one for quick testing only
            # print(temp_df.dtypes)
        else:
            # Display a message to indicate the file extension found is not able to be converted at this time
            # input(f"This file format is not available to be converted at this time: {agency}. Please press Enter to "
            # f"continue...")
            # USE THE ONE THAT FOLLOWS
            # ctypes.windll.user32.MessageBoxW(0, f"This file format is not available"
            #                                     f" to be converted at this time: {agency}", "Extension Error", 1)
            print(f"The following file cannot be translated currently: {agency}")

    # Now we will attempt to concatenate our list of dataframes into one
    df = pd.concat(li, axis=0)
    # print(f"The shape of the simple joined dataframe is: {df.shape}")
    # df.head()

    # Does above but for the data with the removed columns
    df2 = pd.concat(liz, axis=0)
    df2.reset_index(drop=True, inplace=True)

    uid = "CR"  # This is the uid for the project
    now = date.today()

    # print(f"The shape of the modified and intersected dataframe is: {df2.shape}")
    df2.index = df2.index.astype(str)
    df2.index.name = 'uid'
    df2.index = f"{uid}-{now}-" + df2.index
    # print(df2.index)
    # df.head()

    # df.to_csv(f"{opath.directory}/SingleFile.csv")  # This is the production code
    # df2.to_csv(f"{opath.directory}/zzSingleFile.csv")  # This is the production code
    df.to_csv(f"{opath}/SingleFile.csv")  # Testing purposes only
    df2.to_csv(f"{opath}/zzSingleFile.csv")  # Testing purposes only
    print('')
    print('The merged document contains the following columns:')
    for (columnName) in df2.columns:  # columnName inside a for loop works just as well.
        print(columnName)
    print('')
    print('')
    print('The following is the first 5 rows from the combined data:')
    print(tabulate(df2.head(5), headers='keys', tablefmt='psql'))
    print("The process is complete.")
    quit()


if __name__ == "__main__":
    main()
