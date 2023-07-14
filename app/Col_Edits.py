import pandas as pd
import tkinter as tk
import re


# This function renames the columns based on an external spreadsheet that the user must update to ensure the data
# standard is met. If the agency does not exist within the spreadsheet the system will not rename any columns.
# The current function also deletes the columns that are not a part of the data standard. An original copy of the data
# is saved prior to the function being called. A future update should include a second copy that is only the agency
# specific columns for future analysis or future reference.
def replace_column_names(df_a, df_b, row_index):  # This function renames the columns based on an external spreadsheet
    win = tk.Tk()
    win.geometry("")
    win.withdraw()

    # Make a copy of the dataframe to not mess with the original
    temp_df = df_a.copy()
    specific_df = df_a.copy()

    try:
        # Get the values from the correct agency row DataFrame B (agency reference)
        column_name_check = df_b.loc[row_index].values
        # Create a list to map column names from DataFrame A to DataFrame B
        new_columns = []
        specific_columns = []
        # Iterate over columns in DataFrame A
        for col in temp_df:
            # Check if the column name is present in the desired column names from DataFrame B
            if col in column_name_check:
                # Get the index of the column name in column_names
                index = list(column_name_check).index(col)
                new_columns.append(df_b.columns[index])
                specific_df.drop(col, axis=1, inplace=True)
            else:
                # If the column name is not present in column_names, keep the original column name
                specific_columns.append(col)  # This captures the column and stores it for the specific agency file
                temp_df.drop(col, axis=1, inplace=True)

        # Rename columns in DataFrame A using the new columns list
        temp_df.columns = new_columns
        specific_df.columns = specific_columns

        if 'City' in temp_df:
            print("There is already city information")
        else:
            temp_df.insert(0, 'City CFS', df_b.loc[row_index, 'City CFS'])

        if 'State' in temp_df:
            print("There is already state information")
        else:
            temp_df.insert(0, 'State CFS', df_b.loc[row_index, 'State CFS'])

    except KeyError:
        print("That agency is not listed in the reference")

    return temp_df, specific_df


def date_edits(primary_df):
    temp_df = primary_df.copy()

    # By priority, process call date/time columns
    if 'Call Date/Time' in temp_df.columns:
        temp_df['Call Date/Time'] = pd.to_datetime(temp_df['Call Date/Time'],
                                                   format='mixed').dt.strftime('%Y-%m-%d %H:%M:%S')
        if 'Call Date' in temp_df.columns:
            temp_df.drop('Call Date', axis=1, inplace=True)
        if 'Call Time' in temp_df.columns:
            temp_df.drop('Call Time', axis=1, inplace=True)
    elif 'Call Date' in temp_df.columns and 'Call Time' in temp_df.columns:
        temp_df['Call Date/Time'] = temp_df['Call Date'].astype(str) + ' ' + temp_df['Call Time'].astype(str)
        temp_df['Call Date/Time'] = pd.to_datetime(temp_df['Call Date/Time'],
                                                   format='mixed').dt.strftime('%Y-%m-%d %H:%M:%S')
        temp_df.drop('Call Date', axis=1, inplace=True)
        temp_df.drop('Call Time', axis=1, inplace=True)
    else:
        print("No Call Date/Time information available")

    # By priority process dispatch date/time columns
    if 'Dispatch Date/Time' in temp_df.columns:
        temp_df['Dispatch Date/Time'] = pd.to_datetime(temp_df['Dispatch Date/Time'],
                                                       format='mixed').dt.strftime('%Y-%m-%d %H:%M:%S')
        if 'Dispatch Date' in temp_df.columns:
            temp_df.drop('Dispatch Date', axis=1, inplace=True)
        if 'Dispatch Time' in temp_df.columns:
            temp_df.drop('Dispatch Time', axis=1, inplace=True)
    elif 'Dispatch Date' in temp_df.columns and 'Dispatch Time' in temp_df.columns:
        temp_df['Dispatch Date/Time'] = temp_df['Dispatch Date'].astype(str) + ' ' + \
                                        temp_df['Dispatch Time'].astype(str)
        temp_df['Dispatch Date/Time'] = pd.to_datetime(temp_df['Dispatch Date/Time'],
                                                       format='mixed').dt.strftime('%Y-%m-%d %H:%M:%S')
        temp_df.drop('Dispatch Date', axis=1, inplace=True)
        temp_df.drop('Dispatch Time', axis=1, inplace=True)

    else:
        print("No Dispatch Date/Time information available")

    return temp_df


def auid_addition(primary_df, secondary_df, agency):
    temp1_df = primary_df.copy()
    temp2_df = secondary_df.copy()

    # Create a new column with the file name for the agency at the leftmost portion of the dataframe
    temp1_df.insert(0, 'Agency', agency)
    temp1_df['Agency'] = temp1_df['Agency'].replace('.csv', '', regex=True)

    if 'Agency' in temp2_df:
        temp2_df.insert(0, 'Agency_CFS', agency)
        temp2_df['Agency_CFS'] = temp2_df['Agency_CFS'].replace('.csv', '', regex=True)
    else:
        temp2_df.insert(0, 'Agency', agency)
        temp2_df['Agency'] = temp2_df['Agency'].replace('.csv', '', regex=True)

    # Remove any underscores from the column headers
    temp1_df = temp1_df.rename(columns=lambda name: name.replace('_', ' '))
    temp2_df = temp2_df.rename(columns=lambda name: name.replace('_', ' '))

    # Assign the Agency Unique ID (AUID)
    tindex = temp1_df.index.astype(str)
    auid = f"{agency}-" + tindex
    temp1_df.insert(0, 'auid', auid)

    tindex = temp2_df.index.astype(str)
    auid = f"{agency}-" + tindex
    temp2_df.insert(0, 'auid', auid)

    return temp1_df, temp2_df


def call_type_edit(string):
    if not type(string) == str:
        new_string = str(string)
    else:
        new_string = string
    clean_calltype = re.sub(r'^(=+|-+)', '', new_string)

    # for i in range(len(new_df['call type'])):
    #     clean_calltype = re.sub(r'^(=+|-+)', '', new_df['call type'].iloc[i])
    #     new_df['call type'].iloc[i] = clean_calltype

    return clean_calltype