import requests
import pandas as pd
import time
import argparse
import os

def retrieve_given_publications(authors_file, output_file):
    # Load given authors from Excel file
    given_authors = pd.read_excel(authors_file, header=None).values.flatten().tolist()

    # Initialize an empty DataFrame to store publications
    publications_df = pd.DataFrame(columns=['Title', 'Authors', 'Year', 'Match Status'])

    # Loop through each given author
    for author in given_authors:

        # Make API requests to retrieve publications for the author from two different APIs
        api_url_1 = f'https://dblp.org/search/publ/api?q={author}&format=json&h=1000'
        api_url_2 = f'https://dblp.org/search/publ/api?q={author}&format=json&h=1000&f=1000'
        
        for api_url in [api_url_1, api_url_2]:
            response = requests.get(api_url)

            try:
                # Check if the response contains valid JSON
                data = response.json()
            except requests.exceptions.JSONDecodeError as e:
                print(f"Error decoding JSON for author {author}: {e}")
                print(f"Response content: {response.content}")
                continue  # Skip to the next author if JSON decoding fails

            # Extract relevant information from the API response
            for result in data.get('result', {}).get('hits', {}).get('hit', []):
                title = result.get('info', {}).get('title', '')
                authors_info = result.get('info', {}).get('authors', {}).get('author', [])

                # Handle different author list formats (some are strings, others are lists, and some have unexpected formats)
                if isinstance(authors_info, list):
                    # If authors_info is a list, extract author names
                    matching_authors = [a.get('text', '') for a in authors_info if a.get('text', '') in given_authors]
                else:
                    # If authors_info is a single author, check if it's in given_authors
                    matching_authors = [authors_info.get('text', '')] if authors_info.get('text', '') in given_authors else []

                if matching_authors:
                    authors = ', '.join(matching_authors)
                    match_status = 'Exact Match with given Authors list'
                else:
                    authors = ''
                    match_status = 'No Exact Match Found'

                year = result.get('info', {}).get('year', '')

                # Append the publication information to the DataFrame
                publications_df = pd.concat([publications_df, pd.DataFrame({'Title': [title], 'Authors': [authors], 'Year': [year], 'Match Status': [match_status]})],
                                            ignore_index=True)

            # Introduce a longer delay to avoid exceeding the rate limit (the sleep period can be adjusted based on the API rate limit)
            time.sleep(5)

    # Filter out publications with no matching authors
    publications_df = publications_df[publications_df['Match Status'] != 'No Exact Match Found']

    # Drop duplicate publications based on Title, Authors, and Year
    publications_df = publications_df.drop_duplicates(subset=['Title', 'Authors', 'Year'])

    # Save the DataFrame to an Excel file
    publications_df.to_excel(output_file, index=False)

    # Print some information for debugging
    success_art = r"""  ______   __    __   ______    ______   ________   ______    ______  
 /      \ /  |  /  | /      \  /      \ /        | /      \  /      \ 
/$$$$$$  |$$ |  $$ |/$$$$$$  |/$$$$$$  |$$$$$$$$/ /$$$$$$  |/$$$$$$  |
$$ \__$$/ $$ |  $$ |$$ |  $$/ $$ |  $$/ $$ |__    $$ \__$$/ $$ \__$$/ 
$$      \ $$ |  $$ |$$ |      $$ |      $$    |   $$      \ $$      \ 
 $$$$$$  |$$ |  $$ |$$ |   __ $$ |   __ $$$$$/     $$$$$$  | $$$$$$  |
/  \__$$ |$$ \__$$ |$$ \__/  |$$ \__/  |$$ |_____ /  \__$$ |/  \__$$ |
$$    $$/ $$    $$/ $$    $$/ $$    $$/ $$       |$$    $$/ $$    $$/ 
 $$$$$$/   $$$$$$/   $$$$$$/   $$$$$$/  $$$$$$$$/  $$$$$$/   $$$$$$/  
                                                                      
                                                                      
                                                                      """
    print("\033[92m{}\033[0m".format(success_art))
    print("\033[92mPublications saved to {}\033[0m".format(output_file))
    print("\033[92mNumber of given authors: {}\033[0m".format(len(given_authors)))
    print("\033[92mNumber of publications extracted: {}\033[0m".format(len(publications_df)))



if __name__ == "__main__":
    # Initialize the argument parser
    parser = argparse.ArgumentParser(description="Retrieve given publications and save to an Excel file.")
    
    # Add argument for input authors file
    parser.add_argument("-i", "--input", required=True, help="Path to the input Excel file containing given authors.")
    
    # Parse the command-line arguments
    args = parser.parse_args()

    # Extract the base name of the input file (without extension) and append '_extracted_publications.xlsx' to form the output filename
    input_base_name = os.path.splitext(os.path.basename(args.input))[0]
    output_filename = f"{input_base_name}_extracted_publications.xlsx"

    # Define the directory path where the output file will be saved
    output_dir = 'files'

    # Check if the directory exists, and if not, create it
    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    # Set the output file path using the 'files' directory
    output_file_path = os.path.join(output_dir, output_filename)

    # Call the function using the provided command-line argument and the constructed output file path
    retrieve_given_publications(args.input, output_file_path)
