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