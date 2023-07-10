from geopy.geocoders import Nominatim
import time
import pandas as pd
import re
import CFS

pd.options.mode.chained_assignment = None


def sort_nums(row):
    newlocation = row
    # print(f"Incoming data: {newlocation}")
    numbers = ''

    if pd.isna(newlocation):
        print("No data to convert")

    else:
        newlocation = str(newlocation)
        # print(newlocation)
        numbers = [float(s) for s in re.findall(r'-?\d+\.?\d*', newlocation)]
        numbers.sort(key=lambda x: int(-x))
        print(f"This is the reorder lat/long info: {numbers}")

    return numbers


def search(mydict, lookup):
    for key, value in mydict.items():
        for v in value:
            if lookup in v:
                return key


def location_coding(df):
    dict1 = {}  # Create a blank dictionary

    with open("Dictionary.txt") as f:  # Import the dictionary from the text file
        for line in f:
            key_value = line.rstrip('\n').split(":")
            if len(key_value) == 2:
                dict1[key_value[0]] = key_value[1]

    dict2 = {v: k for k, v in dict1.items()}  # Swap the dictionary around since the city name appeared before the abv.
    # print(dict2)

    working_df = df.copy()
    new_columns = []
    for col in working_df:
        ncol = col  # Sets the new column (ncol) variable to the column name from the dataframe
        ncol = CFS.camel_case_split(ncol)  # Splits the column name based on if CamelCase is present (produces a list)
        ncol = ' '.join(ncol)  # Joins the list back into a single string separated by a space
        ncol = ncol.lower()  # Lowers the string to allow easy comparison to the 'final_columns' list
        ncol = ncol.replace('_', ' ')  # Replaces the underscore with a space to allow better comparison
        # Trying to get the column replaced with approved words
        # print(ncol)
        # print(any(any(ncol in s for s in subList) for subList in dict1.values()))
        # print(search(dict1, ncol))

        # if 'latitude' in ncol:
        #     ncol = 'latitude'
        # elif 'longitude' in ncol:
        #     ncol = 'longitude'
        # elif 'city' in ncol:
        #     working_df = working_df.replace({col: dict2})
        #
        new_columns.append(ncol)

    working_df.columns = new_columns
    # print(working_df.columns)

    # Used to update the city name with something Nominatim can recognize
    # for col in working_df.columns:
    #     ncol = col
    #     ncol = ncol.split()
    #     if 'city' in ncol:
    #         # print("There is a city column")
    #         working_df = working_df.replace({col: dict2})
    #     else:
    #         pass

    # flat_lc = list(itertools.chain(*location_check))

    # By priority, we will conduct geocoding work if necessary. No geocoding is required if Lat/Long information is
    # already given.

    if 'location (lat/long)' in working_df.columns:
        working_df['location (lat/long)'] = working_df['location (lat/long)'].astype(str)
        working_df['location (lat/long)'] = working_df['location (lat/long)'].replace('\(|\)', '', regex=True)
        working_df['location (lat/long)'] = working_df['location (lat/long)'].replace('POINT', '', regex=True)
        for i in range(len(working_df['location (lat/long)'])):
            temp_lat_long = working_df['location (lat/long)'].iloc[i]
            if pd.isna(temp_lat_long):
                pass
            else:
                temp_lat_long = temp_lat_long.split()
                temp_lat_long.sort(reverse=True)
                temp_lat_long = ', '.join(temp_lat_long)
                working_df['location (lat/long)'].iloc[i] = temp_lat_long
            i += 1

    elif 'latitude' in working_df.columns and 'longitude' in working_df.columns:
        print("Merging latitude and longitude information.")
        working_df['location (lat/long)'] = \
            working_df['latitude'].apply(str) + ', ' + working_df['longitude'].apply(str)
        working_df.drop('latitude', axis=1, inplace=True)
        working_df.drop('longitude', axis=1, inplace=True)

    elif 'lat' in working_df.columns and 'long' in working_df.columns:
        print("Merging lat/long information.")
        working_df['location (lat/long)'] = working_df['lat'].apply(str) + ' ' + working_df['long'].apply(str)
        working_df.drop('lat', axis=1, inplace=True)
        working_df.drop('long', axis=1, inplace=True)

    elif 'location' in working_df.columns:
        print("Working through location information.")
        working_df['location'] = working_df['location'].replace('\(|\)', '', regex=True)
        working_df['location'] = working_df['location'].replace('POINT', '', regex=True)
        working_df['location (lat/long)'] = working_df['location']
        working_df['location (lat/long)'] = working_df['location (lat/long)'].apply(lambda row: sort_nums(row))
        working_df.drop('location', axis=1, inplace=True)

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
