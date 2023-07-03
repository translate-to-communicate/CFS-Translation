import CFS
import pandas as pd
from sodapy import Socrata  # This is for the St. Pete API


def api_yn():
    return False


def api_calls(opath, final_columns):
    columns_final = final_columns
    api_li = []
    api_liz = []
    opath = opath
    usrname = "***"
    psword = "***"
    myapptoken = "***"

    # Add the API code here. Be sure to add your API user/pass and token.

    # This is the code for the St. Petersburg, FL Police Department.
    # The API call brings in 16 data fields (id, event_number, event_case_number, type_of_engagement, sub_engagement,
    # classification, display_address, crime_date, crime_time, latitude, longitude, location, submit_an_anonymous_tip,
    # neighborhood_name, council_district, and event_subtype_type_of_event).
    agency = "St. Pete API"
    print(f"Starting {agency}")
    client = Socrata("stat.stpete.org",
                     myapptoken,
                     username=usrname,
                     password=psword)
    # First 2000 results, returned as JSON from API / converted to Python list of
    # dictionaries by sodapy.
    results = client.get("2eks-pg5j", limit=2000)
    # Convert to pandas DataFrame
    results_df = pd.DataFrame.from_records(results)
    results_df.insert(0, 'Agency', agency)
    results_df.to_csv(f"{opath}/01_Original_{agency}.csv", index=False)
    api_li.append(results_df)

    results_df = CFS.col_edit(results_df, columns_final)
    results_df.to_csv(f"{opath}/02_User_Modified_{agency}.csv", index=False)
    results_df = results_df[results_df.columns.intersection(columns_final)]
    api_liz.append(results_df)
    results_df.to_csv(f"{opath}/03_Final_{agency}.csv", index=False)

    # Montgomery County, MD
    agency = "MCPD API"
    print(f"Starting {agency}")
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
    results_df = CFS.col_edit(results_df, columns_final)
    results_df.to_csv(f"{opath}/02_User_Modified_{agency}.csv", index=False)
    results_df = results_df[results_df.columns.intersection(columns_final)]
    api_liz.append(results_df)
    results_df.to_csv(f"{opath}/03_Final_{agency}.csv", index=False)

    # New Orleans, LA Police Department
    agency = "NOPD API"
    print(f"Starting {agency}")
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
    results_df = CFS.col_edit(results_df, columns_final)
    results_df.to_csv(f"{opath}/02_User_Modified_{agency}.csv", index=False)
    results_df = results_df[results_df.columns.intersection(columns_final)]
    api_liz.append(results_df)
    results_df.to_csv(f"{opath}/03_Final_{agency}.csv", index=False)

    return api_li, api_liz
