June 10
 - Added 2 functions "call" and "col_edit" which reduces the overall space of the "main" function
 - Removed excess comments
 - GUI code commented out but left in - working on making a singular window to address all prompts
 - Fixed an issue where if the user did not give the agency an updated name the new file extension was added </br> on top of the old file extension (e.g., .xlsx became .xlsx.csv)

June 13
- Updated the col_edit function to identify "Mandatory" columns based on the global 'final_columns' list
- Added a final message window that will display the first 5 rows of the final document to include the column headers

June 15
- Fixed an error that caused the col_edit loop to end if the user chose to keep a column ('break' used instead of 'pass')
- Added in the API for St. Pete, FL. Successfully pulls data; formatting to follow in future updates.
- Reset the testing branch to fix security issues
- Modified the main file name
- Added additional mandatory columns to the final_columns list: disposition, case, map, subdivision, <br> latitude, longitude, lat, lon.

June 16
- Restructured the file directory
- Added setup.py, __init__.py
- Fixed an error where no file directory chosen would result in the C:/ being chosen by default
- Added run.py to call the primary function to occur
- Removed the .idea folder from the repository

June 20
- Added two functions (input and output directory calls) to reduce code inside the main function. Allows for quicker<br> swapping between test code and production code.
- Added a loop to the col_edit function to skip empty data and provide a useful example for the user
- Created a function to display the percentage of a column that is empty (not currently used)
- Adjusted col_edit to add in a statement showing the percentage of the column that is empty (not currently used)
- Adjusted col_edit to auto-remove columns that contain 'http' or 'https'

June 21
- Function for API calls has been added. A variable in the 'main' function, 'api_option', is set to False by default<br> to skip the call.

June 26
- Created function to generate the final columns from a text file. Removes the global list and allows updating via <br> a .txt file.
- Created a location function to manage the location data

June 27
- Updated location function to merge columns for better processing
- Geocoding struggles with Nominatim

June 28
- Added a dictionary to allow for content replacement during location processing. Nominatim struggled due to an <br> inability to locate the address without the proper city (VAB does not exist - it is Virginia Beach).
- A large issue is the request limit that is placed on the geocoding by the Nominatim Usage Policy. The volume <br> of requests ultimately results in an error "geopy.exc.GeocoderServiceError: Non-successful status code 502".

June 29
- Moved the API and location processing to separate files
- Updated requirements to include geopy
- Updated location script to process various location data by priority / ease of consumption. A lat/long is the <br> desired outcome. However, not all location information currently produces a lat/long. If the agency <br> only provides a block address then the system will not be able to identify its location (even with a zip).

June 30
- Cleaned up the main file
- The api_option variable has been moved to the APIs file to allow a singular point of editing for all API needs

July 3
- Created a new function in LocationProcessing to take the location data provided and convert to the correct <br> lat/long format. Data provided is typically written as "POINT (longitude, latitude)" and needs to be "latitude, longitude"
- Added 3 lines to the main function to assign Agency UIDs based on the Agency information and the index number

July 4
- Small updates to columns text and to the AUID

July 5
- Added Seattle, WA API
- Fixed issue with AUID getting deleted

July 6
- Modified the dataframe (df) to keep columns that have words that match the final columns list (the intersection <br> does only full strings and not individual words)
- Fixed API integration. The separate API script returned a list which caused the list to become a list of lists <br> which the system could not concat
- Modified the API calls to include Timeout error handling.
- Modified the dictionary and created a separate agency specific reference that will be used in future work**
- Updated setup to include additional requirements
- Created a dataframe that will be used for agency specific references - might work better than the dictionary. The <br> user will only need to update the fields as they pertain to the new agencies.
- Created a dictionary that is generated based on an external xlsx file.
- Functions created that: create a dictionary based on an external xlsx file, remove empty values from the <br> dictionary, and rename the headers of the dataframe based on that dictionary.

July 7
- Using a dataframe to properly assign the correct column headers to the agency files based on an external spreadsheet.
- Fixed the "replace_column_name" function to catch KeyError
- Removed unnecessary comments
- Added a dictionary and list that pulls the agency name based on the file. Avoids asking the user questions for <br> agency name unless the name doesn't appear in the dictionary.
- Currently, only 4 key steps are required before a user can run the program.
  - Place all files that are to be used in the same directory
  - Properly name the file based on the file naming convention
  - Update the external spreadsheet to align with the common data standard designed for this system
  - If using an API, update the API file to account for specific API requirements (usr/pass/token etc.)

July 10
- Fixed an issue that was causing concat issues
- Added an AUID function to add the agency column and AUID column
- Created a date_edits function to handle the varied date time formats that are ingested
- Reworked the initial processing of columns from each agency - all agencies will have 12 total columns before the <br> agency and AUID columns are added.
  - Call Date and Call Time are processed, merged, and then dropped
  - Dispatch Date and Dispatch Time are processed, merged, and then dropped
  - Latitude and Longitude are processed, merged, and dropped
  - Agency, Incident Number, Call Type, Call Date/Time, Dispatch Date/Time, Block Address, and Location (Lat/Long) <br> are the columns that will remain at the end of processing. The agency specific columns are separated and stored in a separate file.
- Fixed an issue with some agencies having a double comma in the lat/long

July 11
- Separated the "replace_column_names", "date_edits", and "auid_addition" functions to a separate module
- Modified the date_edits function to delete the "dispatch date", "dispatch time", "call date", "call time" <br> columns after processing
- Modified the LocationProcessing module to delete any latitude and longitude columns after processing
- Current final columns are:
  - UID, AUID, Agency, Incident Number, Call Type, Block Address, Location(Lat/Long), Call Date/Time, Dispatch Date/Time

July 12
- Updated the location service to account for the APIs bringing in extra content to the location (lat/long) column
- Addressed some minor errors in variable names