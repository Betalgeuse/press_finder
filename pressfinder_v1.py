import pandas as pd
import requests
import time
from bs4 import BeautifulSoup
from googlesearch import search
import os

def get_press_release_link(company_name):
    # Search the company name and 'press release' on Google
    query = f"{company_name} press release"

    try:
        # Perform the search
        search_results = search(query, num=3)
        for result in search_results:
            if 'press' in result or 'news' in result or 'media' in result:
                return result
    except Exception as e:
        print(f"An error occurred: {e}")
    return None

def main():
    # Set the input file path
    input_path = "C:/Users/gbdnd/Desktop/pressfinder_v1/workspace/8250_8400.csv"
    
    # Read the CSV file
    df = pd.read_csv(input_path)

    # Create a new column for the press release links
    df['Press Release Link'] = ''

    # Iterate over the company names and find the press release link
    for index, row in df.iterrows():
        company_name = row[0]
        print(f"Processing {company_name}...")

        retry = True
        while retry:
            try:
                link = get_press_release_link(company_name)
                retry = False
            except requests.exceptions.HTTPError as err:
                if err.response.status_code == 429:
                    retry_after = int(err.response.headers.get('Retry-After', 0))
                    print(f"Too many requests, need to wait for {retry_after} seconds.")
                    time.sleep(retry_after)
                else:
                    print(f"An HTTP error occurred: {err}")
                    retry = False

        if link is not None:
            df.at[index, 'Press Release Link'] = link
        else:
            df.at[index, 'Press Release Link'] = "No press release link found"

    # Get the base name of the input file without extension
    base_name = os.path.basename(input_path).split('.')[0]
    number1, number2 = base_name.split('_')

    # Generate the output file name
    output_file_name = f"press_search_{number1}_{number2}.csv"

    # Write the updated DataFrame to a new CSV file
    df.to_csv(output_file_name, index=False)

    print("Done!")

if __name__ == '__main__':
    main()
