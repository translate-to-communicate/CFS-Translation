# Updated 13JUL2023 11:02
# Author: Christopher Romeo
# This is the testing branch
# Agency specification, column selection, .csv and .xlsx fully functional.
# API access started, xml testing started (need a proper xml file).
import tkinter as tk
from tkinter import *
from tkinter.simpledialog import askstring
import tkinter.messagebox as mbox
from tkinter import filedialog
import pandas as pd
from pandas import ExcelFile
from tabulate import tabulate
import os
import glob
import ctypes
from datetime import date
import re

import LocationProcessing
import APIs
import Col_Edits

auto_delete = ['http', 'https', ':@computed']


def reindex_dataframes(li):
    reindexed_dataframes = []
    start_index = 0

    for ndf in li:
        end_index = start_index + len(ndf)
        new_index = pd.RangeIndex(start=start_index, stop=end_index)
        reindexed_df = ndf.set_index(new_index)
        reindexed_dataframes.append(reindexed_df)
        start_index = end_index

    return reindexed_dataframes


def column_creation():
    columns_list = []
    with open("Columns.txt", "r") as f:
        for line in f:
            words = line.strip().split(', ')
            columns_list.extend(words)
    return columns_list


def agency_reference():
    xls = ExcelFile("C:/Users/chris/Desktop/School Assignments/Summer/Agency Reference.xlsx")
    df_dict = xls.parse(xls.sheet_names[0], index_col=0)
    return df_dict


def remove_empty_values(dictionary):
    cleaned_dict = {}
    for key, values in dictionary.items():
        cleaned_values = [value for value in values if value and not pd.isna(value)]
        if cleaned_values:
            cleaned_dict[key] = cleaned_values
    return cleaned_dict


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


# Function to determine the number of empty rows in each column
# def blank_count(df):
#     working_df = df
#     # print(working_df.isna().sum())
#     print(f'{(working_df.isna().mean() * 100).round(2)}')


# Function to allow the user to select specific columns to keep; ones that are not considered mandatory.
# It shows the first line of data from that column with information (blank info is skipped) as an example for the user
def col_edit(df, final_columns, agency):
    twin = tk.Tk()
    twin.withdraw()
    working_df = df
    columns_final = final_columns
    agency_name = agency

    for col in working_df:
        ncol = col  # Sets the new column (ncol) variable to the column name from the dataframe
        ncol = camel_case_split(ncol)  # Splits the column name based on if CamelCase is present (produces a list)
        ncol = ' '.join(ncol)  # Joins the list back into a single string separated by a space
        ncol = ncol.lower()  # Lowers the string to allow easy comparison to the 'final_columns' list
        ncol = ncol.replace('_', ' ')  # Replaces the underscore with a space to allow better comparison
        # print(ncol)  # Displays the final resulting name of the new column for comparison
        # A loop that searches for any matching words from the new column and the 'final_columns' list
        if any(word in ncol for word in columns_final):
            # print(f"{col} column is mandatory.")
            pass
        elif any(word in ncol for word in auto_delete):
            # print(f"{col} column has been auto-removed")
            working_df.drop(col, axis=1, inplace=True)
        else:
            # Display a message that asks to delete the column and provide an example of data in that column
            i = 0
            example = working_df[col].iloc[i]
            example = str(example)

            while pd.isna(working_df[col].iloc[i]):  # The loop will bypass blank data
                i += 1
                example = working_df[col].iloc[i]
                example = str(example)

            if any(word in example for word in auto_delete):
                # print(f"{col} column has been auto-removed.")
                working_df.drop(col, axis=1, inplace=True)
            else:
                # percent_empty = (working_df[col].isna().mean() * 100).round(2)
                # no_to_keep = 'Deleted'

                result = mbox.askyesno(f'{agency_name}', f"Do you want keep the following column: {col}? "
                                                         f"An example of the data in this column is: {example}.")
                # User choice dictates either keeping or deleting the column
                if result:
                    # print('User chose to keep the column')
                    pass
                else:
                    # print(f'Deleting column: {col}')
                    working_df.drop(col, axis=1, inplace=True)
                    # print(no_to_keep)

    return working_df


# Function to present the user with a window to acknowledge completion and provide a small preview of the data generated
def final_message(df):
    def close():
        root.destroy()
        quit()

    root = tk.Tk()
    root.geometry("1500x600")
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

    final_columns = column_creation()
    # Creates the Agency Reference Dataframe
    agency_ref = agency_reference()

    # Open the file explorer to allow the user to select both the input and output directories
    # ipath is the input directory path and opath is the output directory path
    # There will be two versions of this directory information to allow for faster testing

    # Call the functions for input and output directory folders
    # ipath = input_file_directory()  # Production Code
    # opath = output_file_directory()  # Production Code
    ipath = "C:/Users/chris/Desktop/School Assignments/Summer/TEST DATA"  # Quick Testing Code Only
    opath = "C:/Users/chris/Desktop/School Assignments/Summer/TEST OUTCOME"  # Quick Testing Code Only

    # Create a glob to hold the files for processing
    csv_files_csv = glob.glob(ipath + '/*')

    # The following code creates empty lists to store all the dataframes
    li = []  # This list will be the unaltered dataframes
    liz = []  # This list will be the altered dataframes

    # The goal is to bring in each individual file and store it as its own dataframe and not as a large dictionary
    # Here we loop through the list of files previously scanned, read each one into a dataframe, and append to the list
    api_option = APIs.api_yn()  # Set this to True if API calls are being made

    # API call
    if api_option:
        li, liz = APIs.api_calls(opath, agency_ref)
    else:
        print("No API calls")

    # Here I am attempting to make a list of the agency names based on the file
    file_dct = {}
    for f in csv_files_csv:
        agency_name = os.path.basename(f)
        head, sep, tail = agency_name.partition('_')
        file_dct[agency_name] = head
        # print(head)
        # print(agency_name)

    print(file_dct)

    for f in csv_files_csv:
        # Get the filename
        agency = os.path.basename(f)
        print(f"Now processing: {agency}")
        agency_found = False

        # This check is only the file dictionary - not the external spreadsheet / reference sheet
        while agency_found is False:
            if agency in file_dct:
                print(f"Found the agency: {file_dct[agency]}")
                agency = file_dct[agency]
                agency_found = True
            else:
                print("Agency was not found.")
                agency = ask_agency(agency)  # Call the function to ask for user input on the agency name

        # Read in the document based on format
        if ".csv" in f:
            agency = agency.replace(".csv", "")
            temp_df = pd.read_csv(f)
            # Create a new processed sheet for each agency - NO NEW DATA HAS BEEN ADDED AND NO FORMATTING HAS BEEN DONE
            temp_df.to_csv(f"{opath}/01_Original_{agency}.csv", index=False)
            # Clean the data before injecting new content

            # HERE WE WANT TO RUN THE AGENCY REFERENCE DF AGAINST THE NEW SHEET AND RELABEL THE COLUMNS AS DEFINED
            # IN THE EXTERNAL SPREADSHEET. AGENCY SPECIFIC COLUMNS ARE EXTRACTED AND SEPARATED INTO A NEW DF

            temp_df, testing_df = Col_Edits.replace_column_names(temp_df, agency_ref, agency)
            print("This is the updated dataframe according to the data standard:")
            print(tabulate(temp_df.head(5), headers='keys', tablefmt='psql'))
            print("This is the agency specific columns")
            print(tabulate(testing_df.head(5), headers='keys', tablefmt='psql'))

            # Send to date_edits function to process date/time
            temp_df = Col_Edits.date_edits(temp_df)

            # Send the 2 dataframes to the AUID function to assign the AUID and add the agency column
            temp_df, testing_df = Col_Edits.auid_addition(temp_df, testing_df, agency)

            # Add the modified dataframe to the list
            # Only the dataframe that is now in compliance with the data standard is added
            li.append(temp_df)

            # Send to LocationProcessing
            temp_df = LocationProcessing.location_coding(temp_df)
            print("After Location:")
            print(temp_df.head(5))

            # Here I want to ask the user what columns they wish to keep using the col_edit function
            # print(final_columns)
            # temp_df = col_edit(temp_df, final_columns, agency)
            # print("After column edits")
            # print(temp_df.head(5))
            # Now we save the modified agency file to its own separate file
            testing_df.to_csv(f"{opath}/02_Agency_Specific_{agency}.csv", index=False)

            # temp_df = temp_df[temp_df.columns.intersection(final_columns)]
            # print("After intersection")
            # print(temp_df.head(5))

            # Add to the intersected list
            liz.append(temp_df)
            temp_df.to_csv(f"{opath}/03_Final_{agency}.csv", index=False)
            # print(temp_df.dtypes)
        elif ".xlsx" in f:
            agency = agency.replace(".xlsx", "")
            temp_df = pd.read_excel(f)
            # Create a new processed sheet for each agency - NO NEW DATA HAS BEEN ADDED AND NO FORMATTING HAS BEEN DONE
            temp_df.to_csv(f"{opath}/01_Original_{agency}.csv", index=False)
            # Clean the data before injecting new content

            # HERE WE WANT TO RUN THE AGENCY REFERENCE DF AGAINST THE NEW SHEET
            temp_df, testing_df = Col_Edits.replace_column_names(temp_df, agency_ref, agency)
            print("This is the updated dataframe according to the data standard:")
            print(tabulate(temp_df.head(5), headers='keys', tablefmt='psql'))
            print("This is the agency specific columns")
            print(tabulate(testing_df.head(5), headers='keys', tablefmt='psql'))

            # Send to date_edits function to process date/time
            temp_df = Col_Edits.date_edits(temp_df)

            # Send the 2 dataframes to the AUID function to assign the AUID and add the agency column
            temp_df, testing_df = Col_Edits.auid_addition(temp_df, testing_df, agency)

            # Add the modified dataframe to the list
            # Only the dataframe that is now in compliance with the data standard is added
            li.append(temp_df)

            # Send to location service testing
            temp_df = LocationProcessing.location_coding(temp_df)
            print("After Location:")
            print(temp_df.head(5))

            # Now call the function to ask about each column and return the updated dataframe
            # temp_df = col_edit(temp_df, final_columns, agency)
            # print("After column edits")
            # print(temp_df.head(5))

            # Save the modified agency file
            testing_df.to_csv(f"{opath}/02_Agency_Specific_{agency}.csv", index=False)

            # Now we move on to the actual combination of files into one document
            # temp_df = temp_df[temp_df.columns.intersection(final_columns)]
            # print("After intersection")
            # print(temp_df.head(5))

            # Add to the intersected list
            liz.append(temp_df)
            temp_df.to_csv(f"{opath}/03_Final_{agency}.csv", index=False)
            # print(temp_df.dtypes)
        elif ".xml" in f:
            agency = agency.replace(".xml", "")
            temp_df = pd.read_xml(f)
            # Create a new processed sheet for each agency - NO NEW DATA HAS BEEN ADDED AND NO FORMATTING HAS BEEN DONE
            temp_df.to_csv(f"{opath}/01_Original_{agency}.csv", index=False)
            # Clean the data before injecting new content

            # HERE WE WANT TO RUN THE AGENCY REFERENCE DF AGAINST THE NEW SHEET
            temp_df, testing_df = Col_Edits.replace_column_names(temp_df, agency_ref, agency)
            print("This is the updated dataframe according to the data standard:")
            print(tabulate(temp_df.head(5), headers='keys', tablefmt='psql'))
            print("This is the agency specific columns")
            print(tabulate(testing_df.head(5), headers='keys', tablefmt='psql'))

            # Send to date_edits function to process date/time
            temp_df = Col_Edits.date_edits(temp_df)

            # Send the 2 dataframes to the AUID function to assign the AUID and add the agency column
            temp_df, testing_df = Col_Edits.auid_addition(temp_df, testing_df, agency)

            # add it to the updated dataframe to list
            li.append(temp_df)

            # Send to LocationProcessing
            temp_df = LocationProcessing.location_coding(temp_df)
            print("After Location:")
            print(temp_df.head(5))

            # Here I want to ask the user what columns they wish to keep using the col_edit function
            # print(final_columns)
            # temp_df = col_edit(temp_df, final_columns, agency)
            # print("After column edits")
            # print(temp_df.head(5))

            # Now we save the modified agency file to its own separate file
            temp_df.to_csv(f"{opath}/02_Agency_Specific_{agency}.csv", index=False)

            # temp_df = temp_df[temp_df.columns.intersection(final_columns)]
            # print("After intersection")
            # print(temp_df.head(5))

            # Add to the intersected list
            liz.append(temp_df)
            temp_df.to_csv(f"{opath}/03_Final_{agency}.csv", index=False)
            # print(temp_df.dtypes)
        else:
            # Display a message to indicate the file extension found is not able to be converted at this time
            ctypes.windll.user32.MessageBoxW(0, f"This file format is not available"
                                                f" to be converted at this time: {agency}", "Extension Error", 1)
            # print(f"The following file cannot be translated currently: {agency}")
    # print(li)

    # Now we will attempt to concatenate our list of dataframes into one
    # print("Now we start the final process - concat")
    # reindexed_dataframes = reindex_dataframes(li)
    # # print(reindexed_dataframes)
    # for df in reindexed_dataframes:
    #     print(df.index.tolist())
    # !!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!
    # IT IS BREAKING HERE - IT DOES REDO THE INDEX FOR ALL THE DFS BUT IT WON'T CONCAT
    #
    # df = pd.concat(reindexed_dataframes, axis=0)
    # print(df.head(100))

    # Does above but for the data with the removed columns
    reindexed_dataframes = reindex_dataframes(liz)
    # print(liz)
    df2 = pd.concat(reindexed_dataframes, axis=0)
    # print(df2.head(100))
    df2.reset_index(drop=True, inplace=True)

    # # Trying to get teh final columns to include anything that has the word
    # for col in df.columns:
    #     new_col = col
    #     if any(word in new_col for word in final_columns):
    #         print(f"This column will remain: {new_col}")
    #     else:
    #         df.drop(col, axis=1, inplace=True)

    uid = "CR"  # This is the uid for the project
    now = date.today()

    df2.index = df2.index.astype(str)
    df2.index.name = 'uid'
    df2.index = f"{uid}-{now}-" + df2.index

    # df2 = Col_Edits.call_type_edit(df2)
    df2['call type'] = df2['call type'].apply(Col_Edits.call_type_edit)

    # df.to_csv(f"{opath}/SingleFile.csv")
    df2.to_csv(f"{opath}/00_Final_Archival.csv")
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
    quit()


if __name__ == "__main__":
    main()
