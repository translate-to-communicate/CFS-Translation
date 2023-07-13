import requests
import Col_Edits
import LocationProcessing
import pandas as pd
from sodapy import Socrata  # This is for the St. Pete API
from tabulate import tabulate


def api_yn():
    return False


def api_calls(opath, agency_ref):
    api_agency_ref = agency_ref
    api_li = []
    api_liz = []
    opath = opath
    usrname = "****"
    psword = "****"
    myapptoken = "****"

    # Add the API code here. Be sure to add your API user/pass and token.

    # This is the code for the St. Petersburg, FL Police Department.
    # The API call brings in 16 data fields (id, event_number, event_case_number, type_of_engagement, sub_engagement,
    # classification, display_address, crime_date, crime_time, latitude, longitude, location, submit_an_anonymous_tip,
    # neighborhood_name, council_district, and event_subtype_type_of_event).
    agency = "St.Pete API"
    print(f"Starting {agency}")
    client = Socrata("stat.stpete.org",
                     myapptoken,
                     username=usrname,
                     password=psword)
    # First 100 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    try:
        results = client.get("2eks-pg5j", limit=100)
        # Convert to pandas DataFrame
        results_df = pd.DataFrame.from_records(results)
        # Save the original data
        results_df.to_csv(f"{opath}/01_Original_{agency}.csv", index=False)

        results_df, testing_df = Col_Edits.replace_column_names(results_df, api_agency_ref, agency)
        print("This is the updated dataframe according to the data standard:")
        print(tabulate(results_df.head(5), headers='keys', tablefmt='psql'))
        print("This is the agency specific columns")
        print(tabulate(testing_df.head(5), headers='keys', tablefmt='psql'))

        # Send to date_edits function to process date/time
        results_df = Col_Edits.date_edits(results_df)

        # Send the 2 dataframes to the AUID function to assign the AUID and add the agency column
        results_df, testing_df = Col_Edits.auid_addition(results_df, testing_df, agency)

        # results_df.insert(0, 'Agency', agency)

        api_li.append(results_df)

        results_df = LocationProcessing.location_coding(results_df)
        print("After Location:")
        print(results_df.head(5))

        # results_df = CFS.col_edit(results_df, columns_final)
        testing_df.to_csv(f"{opath}/02_Agency_Specific_{agency}.csv", index=False)
        # results_df = results_df[results_df.columns.intersection(columns_final)]

        api_liz.append(results_df)

        results_df.to_csv(f"{opath}/03_Final_{agency}.csv", index=False)
    except requests.Timeout:
        print("Connection to St. Pete failed.")
    except requests.RequestException:
        print("Unknown Error")

    # Montgomery County, MD
    agency = "MCPD API"
    print(f"Starting {agency}")
    client = Socrata("data.montgomerycountymd.gov",
                     myapptoken,
                     username=usrname,
                     password=psword)
    # First 100 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    try:
        results = client.get("98cc-bc7d", limit=100)
        # Convert to pandas DataFrame
        results_df = pd.DataFrame.from_records(results)
        # Save the original data
        results_df.to_csv(f"{opath}/01_Original_{agency}.csv", index=False)

        results_df, testing_df = Col_Edits.replace_column_names(results_df, api_agency_ref, agency)
        print("This is the updated dataframe according to the data standard:")
        print(tabulate(results_df.head(5), headers='keys', tablefmt='psql'))
        print("This is the agency specific columns")
        print(tabulate(testing_df.head(5), headers='keys', tablefmt='psql'))

        # Send to date_edits function to process date/time
        results_df = Col_Edits.date_edits(results_df)

        # Send the 2 dataframes to the AUID function to assign the AUID and add the agency column
        results_df, testing_df = Col_Edits.auid_addition(results_df, testing_df, agency)

        # results_df.insert(0, 'Agency', agency)

        api_li.append(results_df)

        results_df = LocationProcessing.location_coding(results_df)
        print("After Location:")
        print(results_df.head(5))

        # results_df = CFS.col_edit(results_df, columns_final)
        testing_df.to_csv(f"{opath}/02_Agency_Specific_{agency}.csv", index=False)
        # results_df = results_df[results_df.columns.intersection(columns_final)]

        api_liz.append(results_df)

        results_df.to_csv(f"{opath}/03_Final_{agency}.csv", index=False)
    except requests.Timeout:
        print("Connection to MCPD failed.")
    except requests.RequestException:
        print("Unknown Error")

    # New Orleans, LA Police Department
    agency = "NOPD API"
    print(f"Starting {agency}")
    client = Socrata("data.nola.gov",
                     myapptoken,
                     username=usrname,
                     password=psword)
    # First 100 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    try:
        results = client.get("nci8-thrr", limit=100)
        # Convert to pandas DataFrame
        results_df = pd.DataFrame.from_records(results)
        # Save the original data
        results_df.to_csv(f"{opath}/01_Original_{agency}.csv", index=False)

        results_df, testing_df = Col_Edits.replace_column_names(results_df, api_agency_ref, agency)
        print("This is the updated dataframe according to the data standard:")
        print(tabulate(results_df.head(5), headers='keys', tablefmt='psql'))
        print("This is the agency specific columns")
        print(tabulate(testing_df.head(5), headers='keys', tablefmt='psql'))

        # Send to date_edits function to process date/time
        results_df = Col_Edits.date_edits(results_df)

        # Send the 2 dataframes to the AUID function to assign the AUID and add the agency column
        results_df, testing_df = Col_Edits.auid_addition(results_df, testing_df, agency)

        # results_df.insert(0, 'Agency', agency)

        api_li.append(results_df)

        results_df = LocationProcessing.location_coding(results_df)
        print("After Location:")
        print(results_df.head(5))

        # results_df = CFS.col_edit(results_df, columns_final)
        testing_df.to_csv(f"{opath}/02_Agency_Specific_{agency}.csv", index=False)
        # results_df = results_df[results_df.columns.intersection(columns_final)]

        api_liz.append(results_df)

        results_df.to_csv(f"{opath}/03_Final_{agency}.csv", index=False)
    except requests.Timeout:
        print("Connection to NOPD failed.")
    except requests.RequestException:
        print("Unknown Error")

    # Seattle, WA PD
    agency = "Seattle API"
    print(f"Starting {agency}")
    client = Socrata("data.seattle.gov",
                     myapptoken,
                     username=usrname,
                     password=psword)
    # First 100 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    try:
        results = client.get("33kz-ixgy", limit=100)
        # Convert to pandas DataFrame
        results_df = pd.DataFrame.from_records(results)
        # Save the original data
        results_df.to_csv(f"{opath}/01_Original_{agency}.csv", index=False)

        results_df, testing_df = Col_Edits.replace_column_names(results_df, api_agency_ref, agency)
        print("This is the updated dataframe according to the data standard:")
        print(tabulate(results_df.head(5), headers='keys', tablefmt='psql'))
        print("This is the agency specific columns")
        print(tabulate(testing_df.head(5), headers='keys', tablefmt='psql'))

        # Send to date_edits function to process date/time
        results_df = Col_Edits.date_edits(results_df)

        # Send the 2 dataframes to the AUID function to assign the AUID and add the agency column
        results_df, testing_df = Col_Edits.auid_addition(results_df, testing_df, agency)

        # results_df.insert(0, 'Agency', agency)

        api_li.append(results_df)

        results_df = LocationProcessing.location_coding(results_df)
        print("After Location:")
        print(results_df.head(5))

        # results_df = CFS.col_edit(results_df, columns_final)
        testing_df.to_csv(f"{opath}/02_Agency_Specific_{agency}.csv", index=False)
        # results_df = results_df[results_df.columns.intersection(columns_final)]

        api_liz.append(results_df)

        results_df.to_csv(f"{opath}/03_Final_{agency}.csv", index=False)
    except requests.Timeout:
        print("Connection to Seattle PD failed.")
    except requests.RequestException:
        print("Unknown Error")

    # Fort Lauderdale, FL
    agency = "Fort Lauderdale API"
    print(f"Starting {agency}")
    client = Socrata("fortlauderdale.data.socrata.com",
                     myapptoken,
                     username=usrname,
                     password=psword)
    # First 100 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    try:
        results = client.get("d7g7-86hw", limit=100)
        # Convert to pandas DataFrame
        results_df = pd.DataFrame.from_records(results)
        # Save the original data
        results_df.to_csv(f"{opath}/01_Original_{agency}.csv", index=False)

        results_df, testing_df = Col_Edits.replace_column_names(results_df, api_agency_ref, agency)
        print("This is the updated dataframe according to the data standard:")
        print(tabulate(results_df.head(5), headers='keys', tablefmt='psql'))
        print("This is the agency specific columns")
        print(tabulate(testing_df.head(5), headers='keys', tablefmt='psql'))

        # Send to date_edits function to process date/time
        results_df = Col_Edits.date_edits(results_df)

        # Send the 2 dataframes to the AUID function to assign the AUID and add the agency column
        results_df, testing_df = Col_Edits.auid_addition(results_df, testing_df, agency)

        # results_df.insert(0, 'Agency', agency)

        api_li.append(results_df)

        results_df = LocationProcessing.location_coding(results_df)
        print("After Location:")
        print(results_df.head(5))

        # results_df = CFS.col_edit(results_df, columns_final)
        testing_df.to_csv(f"{opath}/02_Agency_Specific_{agency}.csv", index=False)
        # results_df = results_df[results_df.columns.intersection(columns_final)]

        api_liz.append(results_df)

        results_df.to_csv(f"{opath}/03_Final_{agency}.csv", index=False)
    except requests.Timeout:
        print("Connection to Fort Lauderdale PD failed.")
    except requests.RequestException:
        print("Unknown Error")

    return api_li, api_liz
