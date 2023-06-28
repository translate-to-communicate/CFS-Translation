# Updated 21JUN2023 11:11
# Author: Christopher Romeo
# This is the testing branch
# Agency specification, column selection, .csv and .xlsx fully functional.
# API access started, xml testing started (need a proper xml file).
import sys
import time
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
import easygui as eg
import re
from sodapy import Socrata  # This is for the St. Pete API
import geopy
from geopy.geocoders import Nominatim
import json
import requests
import urllib.parse

# with open("Columns.txt", 'r') as f:
#     columns_file = [line.split(',') for line in f.read().splitlines()]

auto_delete = ['http', 'https', ':@computed']


def geocoding(address):
    # time.sleep(2)
    geolocator = Nominatim(user_agent="CFS_User")
    location = address
    # print(location)

    if pd.isna(location):
        print("No address")
    else:
        print(location)
        # try:
        #     loc = geolocator.geocode(location, timeout=10)
        #     print(location, loc.latitude, loc.longitude)
        # except (AttributeError, KeyError, ValueError):
        #     print(location)
        #     print("No result")

    # return

# new_address = address
# url = 'https://nominatim.openstreetmap.org/search/' + urllib.parse.quote(new_address) + '?format=json'
# response = requests.get(url).json()
# print(response[0]["lat"])
# print(response[0]["lon"])


def location_coding(df):
    dict1 = {}
    with open("Dictionary.txt") as f:
        for line in f:
            key_value = line.rstrip('\n').split(":")
            if len(key_value) == 2:
                dict1[key_value[0]] = key_value[1]
    print(dict1)

    working_df = df
    new_columns = []

    for col in working_df:
        ncol = col  # Sets the new column (ncol) variable to the column name from the dataframe
        ncol = camel_case_split(ncol)  # Splits the column name based on if CamelCase is present (produces a list)
        ncol = ' '.join(ncol)  # Joins the list back into a single string separated by a space
        ncol = ncol.lower()  # Lowers the string to allow easy comparison to the 'final_columns' list
        ncol = ncol.replace('_', ' ')  # Replaces the underscore with a space to allow better comparison
        new_columns.append(ncol)

    working_df.columns = new_columns

    for col in working_df.columns:
        ncol = col
        ncol = ncol.split()
        if 'city' in ncol:
            print("There is a city column")
            working_df = working_df.replace({col: dict1})
        else:
            pass

    # By priority, we will conduct geocoding work if necessary. No geocoding is required if Lat/Long information is
    # already given.
    if 'latitude' in working_df.columns and 'longitude' in working_df.columns:
        print("Merging latitude and longitude information.")
        working_df['Location (Lat/Long)'] = \
            working_df['latitude'].apply(str) + ', ' + working_df['longitude'].apply(str)

    elif 'lat' in working_df.columns and 'long' in working_df.columns:
        print("Merging lat/long information.")
        working_df['Location (Lat/Long)'] = working_df['lat'].apply(str) + ', ' + working_df['long'].apply(str)

    elif 'block address' in working_df.columns and 'city name' in working_df.columns:
        print("Converting Block Address and City Name to a Lat/Long.")
        working_df['Merged Block and City'] = working_df['block address'] + ', ' + working_df['city name']
        # print(working_df['Merged Block and City'].iloc[0])
        working_df['Geocoded Lat/Long'] = working_df['Merged Block and City'].apply(lambda row: geocoding(row))

    elif 'city' in working_df.columns and 'state' in working_df.columns:
        # temp_df.insert(3, 'merged location', (temp_df['block address'] + ' : ' + temp_df['location']))
        print("Merging city and state information.")
        working_df['city and state'] = working_df['city'] + ', ' + working_df['state']
    else:
        print("No location information available")

    return working_df


def column_creation():
    columns_list = []
    with open("Columns.txt", "r") as f:
        for line in f:
            words = line.strip().split(', ')
            columns_list.extend(words)
    return columns_list


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
def blank_count(df):
    working_df = df
    # print(working_df.isna().sum())
    print(f'{(working_df.isna().mean() * 100).round(2)}')


# Function to allow the user to select specific columns to keep; ones that are not considered mandatory.
# It shows the first line of data from that column with information (blank info is skipped) as an example for the user
def col_edit(df, final_columns):
    twin = tk.Tk()
    twin.withdraw()
    working_df = df
    columns_final = final_columns

    for col in working_df:
        ncol = col  # Sets the new column (ncol) variable to the column name from the dataframe
        ncol = camel_case_split(ncol)  # Splits the column name based on if CamelCase is present (produces a list)
        ncol = ' '.join(ncol)  # Joins the list back into a single string separated by a space
        ncol = ncol.lower()  # Lowers the string to allow easy comparison to the 'final_columns' list
        ncol = ncol.replace('_', ' ')  # Replaces the underscore with a space to allow better comparison
        # print(ncol)  # Displays the final resulting name of the new column for comparison
        # A loop that searches for any matching words from the new column and the 'final_columns' list
        if any(word in ncol for word in columns_final):
            print(f"{col} column is mandatory.")
        elif any(word in ncol for word in auto_delete):
            print(f"{col} column has been auto-removed")
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
                print(f"{col} column has been auto-removed.")
                working_df.drop(col, axis=1, inplace=True)
            else:
                # percent_empty = (working_df[col].isna().mean() * 100).round(2)
                # no_to_keep = 'Deleted'
                result = mbox.askyesno('Column Selection', f"Do you want keep the following column: {col}? "
                                                           f"An example of the data in this column is: {example}.")
                # User choice dictates either keeping or deleting the column
                if result:
                    # print('User chose to keep the column')
                    pass
                else:
                    print(f'Deleting column: {col}')
                    working_df.drop(col, axis=1, inplace=True)
                    # print(no_to_keep)

    return working_df


# presents a checkbox that the user can select multiple columns. Limited to only 3 choices which is not useful
def checkbox(df):
    working_df = df
    li = working_df.columns.values.tolist()

    question = "Which columns do you wish to keep?"
    title = "Column Selection"
    list_of_options = li

    choice = eg.multchoicebox(question, title, list_of_options, preselect=None)

    print(choice)


# Function for API calls.
def api_calls(opath, final_columns):
    columns_final = final_columns
    api_li = []
    api_liz = []
    opath = opath
    usrname = "***"
    psword = "****"
    myapptoken = "*****"

    # Add the API code here. Be sure to add your API user/pass and token.

    # This is the code for the St. Petersburg, FL Police Department.
    # The API call brings in 16 data fields (id, event_number, event_case_number, type_of_engagement, sub_engagement,
    # classification, display_address, crime_date, crime_time, latitude, longitude, location, submit_an_anonymous_tip,
    # neighborhood_name, council_district, and event_subtype_type_of_event).
    # There is additional data fields that need to be excluded, but have not yet.
    agency = "St. Pete API"
    client = Socrata("stat.stpete.org",
                     myapptoken,
                     username=usrname,
                     password=psword)
    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("2eks-pg5j", limit=2000)
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    results_df.to_csv(f"{opath}/01_Original_{agency}.csv", index=False)
    api_li.append(results_df)
    results_df = col_edit(results_df, columns_final)
    results_df.to_csv(f"{opath}/02_User_Modified_{agency}.csv", index=False)
    results_df = results_df[results_df.columns.intersection(columns_final)]
    api_liz.append(results_df)
    results_df.to_csv(f"{opath}/03_Final_{agency}.csv", index=False)

    # Montgomery County, MD
    agency = "MCPD API"
    client = Socrata("data.montgomerycountymd.gov",
                     myapptoken,
                     username=usrname,
                     password=psword)
    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("98cc-bc7d", limit=2000)
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    results_df.to_csv(f"{opath}/01_Original_{agency}.csv", index=False)
    api_li.append(results_df)
    results_df = col_edit(results_df, columns_final)
    results_df.to_csv(f"{opath}/02_User_Modified_{agency}.csv", index=False)
    results_df = results_df[results_df.columns.intersection(columns_final)]
    api_liz.append(results_df)
    results_df.to_csv(f"{opath}/03_Final_{agency}.csv", index=False)

    # New Orleans, LA Police Department
    agency = "NOPD API"
    client = Socrata("data.nola.gov",
                     myapptoken,
                     username=usrname,
                     password=psword)
    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("nci8-thrr", limit=2000)
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    results_df.to_csv(f"{opath}/01_Original_{agency}.csv", index=False)
    api_li.append(results_df)
    results_df = col_edit(results_df, columns_final)
    results_df.to_csv(f"{opath}/02_User_Modified_{agency}.csv", index=False)
    results_df = results_df[results_df.columns.intersection(columns_final)]
    api_liz.append(results_df)
    results_df.to_csv(f"{opath}/03_Final_{agency}.csv", index=False)

    return api_li, api_liz


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
    print(final_columns)
    # Open the file explorer to allow the user to select both the input and output directories
    # ipath is the input directory path and opath is the output directory path
    # There will be two versions of this directory information to allow for faster testing

    # Call the functions for input and output directory folders
    # ipath = input_file_directory()  # Production Code
    # opath = output_file_directory()  # Production Code
    ipath = "C:/Users/chris/Desktop/School Assignments/Summer/TEST DATA"  # Quick Testing Code Only
    opath = "C:/Users/chris/Desktop/School Assignments/Summer/TEST OUTCOME"  # Quick Testing Code Only
    api_option = False  # Set this to True if API calls are being made

    # Create a glob to hold the files for processing
    csv_files_csv = glob.glob(ipath + '/*')

    # Show all the files that were identified
    # for file in csv_files_csv:
    #   print(file)

    # The following code creates empty lists to store all the dataframes
    li = []  # This list will be the unaltered dataframes
    liz = []  # This list will be the altered dataframes

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
            temp_df.to_csv(f"{opath}/01_Original_{agency}.csv", index=False)
            # add it to the list
            li.append(temp_df)
            # Testing the location coding
            new_df = location_coding(temp_df)
            print(new_df.head(10))
            # Determine the number of empty cells per column
            # blank_count(temp_df)
            # Here I want to ask the user what columns they wish to keep using the col_edit function
            temp_df = col_edit(temp_df, final_columns)
            # Now we save the modified agency file to its own separate file
            temp_df.to_csv(f"{opath}/02_User_Modified_{agency}.csv", index=False)
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
            temp_df.to_csv(f"{opath}/03_Final_{agency}.csv", index=False)
            # print(temp_df.dtypes)
        elif ".xlsx" in f:
            # Run the same process as above but for Excel files
            temp_df = pd.read_excel(f)
            agency = agency.replace(".xlsx", "")
            temp_df.insert(0, 'Agency', agency)
            temp_df['Agency'] = temp_df['Agency'].replace('.xlsx', '', regex=True)
            temp_df.to_csv(f"{opath}/01_Original_{agency}.csv", index=False)
            li.append(temp_df)
            # Location service testing
            new_df = location_coding(temp_df)
            print(new_df.head(10))
            # Now call the function to ask about each column and return the updated dataframe
            temp_df = col_edit(temp_df, final_columns)
            # print(f'Successfully created dataframe for {agency} with shape {temp_df.shape}')
            temp_df.to_csv(f"{opath}/02_User_Modified_{agency}.csv", index=False)
            # Now we move on to the actual combination of files into one document
            temp_df.columns = map(str.lower, temp_df.columns)
            temp_df = temp_df[temp_df.columns.intersection(final_columns)]
            liz.append(temp_df)
            temp_df.to_csv(f"{opath}/03_Final_{agency}.csv", index=False)
            # print(temp_df.dtypes)
        elif ".xml" in f:
            # Run the same process as above but for XML files
            temp_df = pd.read_xml(f)
            agency = agency.replace(".xml", "")
            temp_df.insert(0, 'Agency', agency)
            temp_df['Agency'] = temp_df['Agency'].replace('.xml', '', regex=True)
            temp_df.to_csv(f"{opath}/01_Original_{agency}.csv", index=False)
            li.append(temp_df)
            temp_df = col_edit(temp_df, final_columns)
            # Now we move on to the actual combination of files into one document
            temp_df.to_csv(f"{opath}/02_User_Modified_{agency}.csv", index=False)
            temp_df.columns = map(str.lower, temp_df.columns)
            temp_df = temp_df[temp_df.columns.intersection(final_columns)]
            liz.append(temp_df)
            temp_df.to_csv(f"{opath}/03_Final_{agency}.csv", index=False)
            # print(temp_df.dtypes)
        else:
            # Display a message to indicate the file extension found is not able to be converted at this time
            ctypes.windll.user32.MessageBoxW(0, f"This file format is not available"
                                                f" to be converted at this time: {agency}", "Extension Error", 1)
            # print(f"The following file cannot be translated currently: {agency}")
    # API call
    if api_option:
        api_li, api_liz = api_calls(opath, final_columns)
        li.append(api_li)
        liz.append(api_liz)
    else:
        print("No API calls")

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

    df.to_csv(f"{opath}/SingleFile.csv")
    df2.to_csv(f"{opath}/zzSingleFile.csv")
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
