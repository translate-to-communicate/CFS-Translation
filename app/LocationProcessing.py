from geopy.geocoders import Nominatim
import time
import pandas as pd

import CFS


def location_coding(df):
    dict1 = {}  # Create a blank dictionary

    with open("Dictionary.txt") as f:  # Import the dictionary from the text file
        for line in f:
            key_value = line.rstrip('\n').split(":")
            if len(key_value) == 2:
                dict1[key_value[0]] = key_value[1]
    # print(dict1)

    dict2 = {v: k for k, v in dict1.items()}  # Swap the dictionary around since the city name appeared before the abv.
    # print(dict2)

    working_df = df
    new_columns = []
    for col in working_df:
        ncol = col  # Sets the new column (ncol) variable to the column name from the dataframe
        ncol = CFS.camel_case_split(ncol)  # Splits the column name based on if CamelCase is present (produces a list)
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
            working_df = working_df.replace({col: dict2})
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
        # Create a new column in the dataframe to store the merged information
        working_df['Merged Block and City'] = working_df['block address'] + ', ' + working_df['city name']
        # Create a new column to store the Lat/Long information
        # Works - commented out to allow faster testing for other processes
        # working_df['Geocoded Lat/Long'] = working_df['Merged Block and City'].apply(lambda row: geocoding(row))

    elif 'city' in working_df.columns and 'state' in working_df.columns:
        # temp_df.insert(3, 'merged location', (temp_df['block address'] + ' : ' + temp_df['location']))
        print("Merging city and state information.")
        working_df['city and state'] = working_df['city'] + ', ' + working_df['state']
    else:
        print("No location information available")

    return working_df


def geocoding(address):
    time.sleep(2)
    geolocator = Nominatim(user_agent="CFS_App")
    location = address
    nlat_long = ''

    if pd.isna(location):
        print("No address")
    else:
        try:
            loc = geolocator.geocode(location, timeout=10)
            if loc is None:
                print(f"Nothing found for: {location}")
            else:
                nlat, nlon = loc.latitude, loc.longitude
                nlat_long = str(f"{nlat}, {nlon}")
                print(f"Service found {nlat_long} for {location}")
        except (AttributeError, KeyError, ValueError):
            print(location, "Error")

    return nlat_long