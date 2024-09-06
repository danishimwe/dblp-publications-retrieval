# DBLP Publications Retrieval Script

## Overview

This Python script is designed to automate the retrieval of authors' publications from DBLP Api. It queries the online DBLP databases using their API  by author names extracted from an Excel file, compiles relevant publication information, and saves the results into an Excel file. This tool is particularly useful for researchers and administrators looking to efficiently gather and organize publications.
There are statements that handle different author list formats (some are strings, others are list and some have unexpected formats).
There is an implementation of dblp sleeping time delay to avoid exceeding the rate limit (the sleep period can be adjusted based on the API rate limit)


## Requirements

- Python 3.6 or higher
- `pandas`
- `requests`
- `openpyxl`
- Excel file with authors listed (one name per row)

## Installation

Before running the script, ensure that you have Python 3.6 or higher installed on your system. You can check your Python version by running:

```bash
python3 --version
```

If you don't have Python installed, download it from the [official Python website](https://www.python.org/downloads/).

Next, install the required Python packages using pip. Run the following command in your terminal:

```bash
pip3 install pandas requests openpyxl
```

## How to Use

1. **Prepare the Authors Excel File**: Create an Excel file containing the names of authors you wish to search for. List each author's name in a separate row in the first column without any headers.

2. **Run the Script**: Navigate to the script's directory in your terminal. Execute the script by specifying the path to your Excel file as follows:

   ```bash
    python3 retrieve_publication.py -i path/to/your_excel_file.xlsx
    ```

    The script automatically creates an output directory named files if it doesn't exist and generates the output Excel file within this directory. The output file is named after the input file, appended with `_extracted_publications.xlsx`.

3. **Review the Output**: Check the `files` directory for the output Excel file. It contains columns for publication titles, authors, publication years, and match statuses with  authors.

## Notes

- The script includes a delay between API requests to avoid exceeding rate limits. This can be adjusted based on the specific requirements of the APIs being queried.
- Ensure that your internet connection is stable during the script's execution to prevent any interruptions during data retrieval.

## Troubleshooting

If you encounter any issues, such as missing packages or errors during execution, verify that all required Python packages are installed and that the Excel file paths are correctly specified. For further assistance, consult the documentation for the `pandas` , `requests` and `openpyxl` libraries or reach out to me for the support.