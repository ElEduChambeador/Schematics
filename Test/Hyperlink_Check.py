import requests
import pandas as pd
from bs4 import BeautifulSoup

def is_valid_url(url):
    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the response status code is 200 (OK)
    if response.status_code == 200:
        # Check if the content does not contain "Error 404" (you can customize this check)
        if "Error 404" not in response.text:
            return True
    return False

def check_hyperlinks(file_path, hyperlink_column):
    # Read the Excel file into a DataFrame
    df = pd.read_excel(file_path)

    # Check if the specified hyperlink column exists in the DataFrame
    if hyperlink_column not in df.columns:
        print(f"Error: '{hyperlink_column}' is not a valid column name.")
        return

    # Iterate through the rows of the DataFrame
    for index, row in df.iterrows():
        hyperlink = str(row[hyperlink_column])

        try:
            # Check if the URL is valid (not an "Error 404" page)
            if is_valid_url(hyperlink):
                print(f"Hyperlink at row {index + 2} in column '{hyperlink_column}' is still available.")
            else:
                print(f"Hyperlink at row {index + 2} in column '{hyperlink_column}' is not available or is an 'Error 404' page.")

        except Exception as e:
            print(f"Error checking hyperlink at row {index + 2} in column '{hyperlink_column}': {str(e)}")

if __name__ == "__main__":
    # Specify the path to your Excel file
    excel_file_path = "C:/Users/063783/Downloads/Master Design Hub Pre Selection Review.xlsx"

    # Print the column names and the first few rows
    df = pd.read_excel(excel_file_path)
    # print("Column names:")
    # for column_name in df.columns:
    #     print(column_name)
    print("\nFirst few rows:")
    print(df.head())
    print()

    # Prompt the user to enter the column name containing hyperlinks
    specified_hyperlink_column = input("Enter the column name containing hyperlinks: ")

    # Call the function to check hyperlinks
    check_hyperlinks(excel_file_path, specified_hyperlink_column)
