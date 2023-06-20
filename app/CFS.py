# Updated 20JUN2023 09:50
# Author: Christopher Romeo
# This is the testing branch
# Agency specification, column selection, .csv and .xlsx fully functional.
# API access started, xml testing started (need a proper xml file).
import sys
import tkinter as tk
from tkinter import *
from tkinter.simpledialog import askstring
import tkinter.messagebox as mbox
from tkinter import filedialog
from tkinter.filedialog import askdirectory
import pandas as pd
from tabulate import tabulate
import numpy as np
import os
import glob
import ctypes
from datetime import datetime, date
import re
from sodapy import Socrata  # This is for the St. Pete API

final_columns = ['agency', 'location', 'priority', 'type', 'code', 'block', 'address', 'date', 'latitude', 'longitude',
                 'area', 'merged location', 'incident', 'close', 'case', 'map', 'subdivision',
                 'disposition', 'lat', 'long', 'classification']


def input_file_directory():
    ipath = Tk()
    ipath.withdraw()
    ipath.directory = filedialog.askdirectory(initialdir="C:/", title="Input Directory for CFS Files")
    while ipath.directory == '':
        result = mbox.askyesno("File Selection Error", "No file directory chosen. Would you like to try again?")
        if result:
            ipath.directory = filedialog.askdirectory(initialdir="C:/", title="Input Directory for CFS Files")
        else:
            quit()
    print('The chosen input directory is: ' + ipath.directory)
    return ipath.directory


def output_file_directory():
    opath = Tk()
    opath.withdraw()
    opath.directory = filedialog.askdirectory(initialdir="C:/", title="Output Directory for CFS Translation Results")
    while opath.directory == '':
        result = mbox.askyesno("File Selection Error", "No file directory chosen. Would you like to try again?")
        if result:
            opath.directory = filedialog.askdirectory(initialdir="C:/", title="Output Directory for CFS Files")
        else:
            quit()
    print('The chosen output directory is: ' + opath.directory)
    return opath.directory


# Function to identify the specific agency for the file being processed. Allows the user to edit the name if needed.
def ask_agency(agency_name):
    win = tk.Tk()
    win.geometry("")
    win.withdraw()
    agency_initial_name = agency_name
    # print(agency_initial_name)
    enta = askstring('Agency', f'What is the responsible agency for the file: {agency_initial_name}?')
    win.destroy()
    if enta == '':
        print(f'No input given for: {agency_initial_name}')
        return agency_initial_name
    elif enta is None:
        print(f'No input is given for: {agency_initial_name}')
        return agency_initial_name
    else:
        print(f'Name has been changed to: {enta}')
        return enta


# Function to split up words that are in CamelCase.
def camel_case_split(identifier):
    matches = re.finditer('.+?(?:(?<=[a-z])(?=[A-Z])|(?<=[A-Z])(?=[A-Z][a-z])|$)', identifier)
    return [m.group(0) for m in matches]


# Function to allow the user to select specific columns to keep; ones that are not considered mandatory.
# It shows the first line of data from that column with information (blank info is skipped) as an example for the user
def col_edit(df):
    twin = tk.Tk()
    twin.withdraw()
    working_df = df

    for col in working_df:
        ncol = col  # Sets the new column (ncol) variable to the column name from the dataframe
        ncol = camel_case_split(ncol)  # Splits the column name based on if CamelCase is present (produces a list)
        ncol = ' '.join(ncol)  # Joins the list back into a single string separated by a space
        ncol = ncol.lower()  # Lowers the string to allow easy comparison to the 'final_columns' list
        ncol = ncol.replace('_', ' ')  # Replaces the underscore with a space to allow better comparison
        # print(ncol)  # Displays the final resulting name of the new column for comparison
        # A loop that searches for any matching words from the new column and the 'final_columns' list
        if any(word in ncol for word in final_columns):
            print(f"{col} column is mandatory")
        else:
            # Display to the user a message that asks to delete the column and provide an example of data in that column
            i = 0
            example = working_df[col].iloc[i]
            while pd.isna(working_df[col].iloc[i]):
                i += 1
                example = working_df[col].iloc[i]

            # no_to_keep = 'Deleted'
            result = mbox.askyesno('Column Selection', f"Do you want keep the following column: {col}?"
                                                       f" An example of the data hosted in this column is: {example}")
            # User choice dictates either keeping or deleting the column
            if result:
                # print('User chose to keep the column')
                pass
            else:
                print(f'Deleting column: {col}')
                working_df.drop(col, axis=1, inplace=True)
                # print(no_to_keep)

    return working_df


# Function to present the user with a window to acknowledge completion and provide a small preview of the data generated
def final_message(df):
    def close():
        root.destroy()
        quit()

    root = tk.Tk()
    root.geometry("1000x600")
    root.title("Final Output Preview")
    final_df = df
    root.protocol('WM_DELETE_WINDOW', close)

    screen = Text(root, height=200, width=900)  # This is the text widget and parameters
    exit_button = Button(root, text="Exit", command=close)  # This is the exit button
    exit_button.pack(side="bottom")
    screen.pack(side="top")

    screen.insert(tk.END, tabulate(final_df.head(5), headers='keys', tablefmt='psql'))

    root.mainloop()


# The main function of the system
def main():
    # The following code was used to enable all the data from a dataframe to be displayed in the run window (PyCharm)
    # The code is a part of the pandas package
    pd.set_option('display.max_rows', None)
    pd.set_option('display.max_columns', None)
    pd.set_option('display.width', None)
    pd.set_option('display.max_colwidth', None)

    # Open the file explorer to allow the user to select both the input and output directories
    # ipath is the input directory path and opath is the output directory path
    # There will be two versions of this directory information to allow for faster testing

    # Call the functions for input and output directory folders
    # ipath = input_file_directory()
    # opath = output_file_directory()
    ipath = "C:/Users/chris/Desktop/School Assignments/Summer/TEST DATA"  # Quick Testing Code Only
    opath = "C:/Users/chris/Desktop/School Assignments/Summer/TEST OUTCOME"  # Quick Testing Code Only

    # Create a glob to hold the files for processing
    csv_files_csv = glob.glob(ipath + '/*')  # This is the production code

    # Show all the files that were identified
    # for file in csv_files_csv:
    #   print(file)

    # The following code creates empty lists to store all the dataframes
    li = []  # This list will be the unaltered dataframes
    liz = []  # This list will be the altered dataframes

    # Call the screen resolution function
    # print(get_curr_screen_geometry())

    # The goal is to bring in each individual file and store it as its own dataframe and not as a large dictionary
    # Here we loop through the list of files previously scanned, read each one into a dataframe, and append to the list
    for f in csv_files_csv:
        # Get the filename
        agency = os.path.basename(f)
        print(f"Now processing: {agency}")
        agency = ask_agency(agency)  # Call the function to ask for user input on the agency name
        # Read in the document based on format
        if ".csv" in f:
            # print("This is a csv file")
            temp_df = pd.read_csv(f)
            agency = agency.replace(".csv", "")
            # Create a new column with the file name for the agency at the leftmost portion of the dataframe
            temp_df.insert(0, 'Agency', agency)
            # data cleaning to remove the .csv
            temp_df['Agency'] = temp_df['Agency'].replace('.csv', '', regex=True)
            # Remove any underscores from the column headers
            temp_df = temp_df.rename(columns=lambda name: name.replace('_', ' '))
            # Create a new processed sheet for each agency
            temp_df.to_csv(f"{opath}/Processed_{agency}.csv", index=False)  # This is the production code
            # add it to the list
            li.append(temp_df)
            # Here I want to ask the user what columns they wish to keep using the col_edit function
            temp_df = col_edit(temp_df)
            # print(temp_df.head(5))  # This shows the first 5 rows of each column in the dataframe
            # Now we save the modified agency file to its own separate file
            temp_df.to_csv(f"{opath}/Agency_Specific_{agency}.csv", index=False)
            # Now make all columns lowercase to allow easier scrub for keywords
            temp_df.columns = map(str.lower, temp_df.columns)
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
            temp_df.to_csv(f"{opath}/zz_{agency}.csv", index=False)  # This is the production code
            # print(temp_df.dtypes)
        elif ".xlsx" in f:
            # Run the same process as above but for Excel files
            temp_df = pd.read_excel(f)
            agency = agency.replace(".xlsx", "")
            temp_df.insert(0, 'Agency', agency)
            temp_df['Agency'] = temp_df['Agency'].replace('.xlsx', '', regex=True)
            temp_df.to_csv(f"{opath}/Processed_{agency}.csv", index=False)  # This is the production code
            li.append(temp_df)
            # Now call the function to ask about each column and return the updated dataframe
            temp_df = col_edit(temp_df)
            # print(temp_df.head(5))
            # print(f'Successfully created dataframe for {agency} with shape {temp_df.shape}')
            temp_df.to_csv(f"{opath}/Agency_Specific_{agency}.csv", index=False)
            # Now we move on to the actual combination of files into one document
            temp_df.columns = map(str.lower, temp_df.columns)
            temp_df = temp_df[temp_df.columns.intersection(final_columns)]
            liz.append(temp_df)
            temp_df.to_csv(f"{opath}/zz_{agency}.csv", index=False)  # This is the production code
            # print(temp_df.dtypes)
        elif ".xml" in f:
            # Run the same process as above but for XML files
            temp_df = pd.read_xml(f)
            agency = agency.replace(".xml", "")
            temp_df.insert(0, 'Agency', agency)
            temp_df['Agency'] = temp_df['Agency'].replace('.xml', '', regex=True)
            temp_df.to_csv(f"{opath}/Processed_{agency}.csv", index=False)  # This is the production code
            li.append(temp_df)
            #
            temp_df = col_edit(temp_df)
            # print(temp_df.head(5))
            # print(f'Successfully created dataframe for {agency} with shape {temp_df.shape}')
            # Now we move on to the actual combination of files into one document
            temp_df.to_csv(f"{opath}/Agency_Specific_{agency}.csv", index=False)
            temp_df.columns = map(str.lower, temp_df.columns)
            temp_df = temp_df[temp_df.columns.intersection(final_columns)]
            liz.append(temp_df)
            temp_df.to_csv(f"{opath}/zz_{agency}.csv", index=False)  # This is the production code
            # print(temp_df.dtypes)
        else:
            # Display a message to indicate the file extension found is not able to be converted at this time
            ctypes.windll.user32.MessageBoxW(0, f"This file format is not available"
                                                f" to be converted at this time: {agency}", "Extension Error", 1)
            # print(f"The following file cannot be translated currently: {agency}")

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

    df.to_csv(f"{opath}/SingleFile.csv")  # This is the production code
    df2.to_csv(f"{opath}/zzSingleFile.csv")  # This is the production code
    print('')
    print('The merged document contains the following columns:')
    for (columnName) in df2.columns:  # columnName inside a for loop works just as well.
        print(columnName)
    print('')
    print('')
    print('The following is the first 5 rows from the combined data:')
    print(tabulate(df2.head(5), headers='keys', tablefmt='psql'))
    final_message(df2)
    # print("The process is complete.")
    # quit()

    # St. Pete API trial run
    # API access works and will pull the first 2000 results
    # Left commented out to reduce the number of API requests during testing
    # myapptoken = "***"
    #
    # client = Socrata("stat.stpete.org",
    #                  myapptoken,
    #                  username="******",
    #                  password="******")
    # # First 2000 results, returned as JSON from API / converted to Python list of
    # # dictionaries by sodapy.
    # results = client.get("2eks-pg5j", limit=2000)
    #
    # # Convert to pandas DataFrame
    # results_df = pd.DataFrame.from_records(results)
    # print(tabulate(results_df.head(10), headers='keys', tablefmt='psql'))
    quit()


if __name__ == "__main__":
    main()
