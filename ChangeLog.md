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