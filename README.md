# DBLP Publications Retrieval Script

## Overview

This Python script is designed to automate the retrieval of authors' publications from the DBLP Api. It queries the online DBLP databases using their API  by author names extracted from an Excel file, compiles relevant publication information, and saves the results into an Excel file. This tool is particularly useful for researchers and administrators looking to efficiently gather and organize publications.
There are statements that handle different author list formats (some are strings, others are list and some have unexpected formats).
There is an implementation of dblp sleeping time delay to avoid exceeding the rate limit (the sleep period can be adjusted based on the API rate limit)


## Requirements

- Python 3.6 or higher
- `pandas`
- `requests`
- `openpyxl`
- `flask`
- Excel file (.csv or .xlsx) with authors listed (First name and Lastname in the same column row {separated with `;`} or listed in the first two columns but same row)

| First name        | Last name |
|-------------------|-----------|
| Firstname;Lastname|           |

    
## Installation

Before running the script, ensure that you have Python 3.6 or higher installed on your system. You can check your Python version by running:

```bash
python3 --version
```

If you don't have Python installed, download it from the [official Python website](https://www.python.org/downloads/).

Next, install the required Python packages using pip. Run the following command in your terminal:

```bash
pip3 install pandas requests openpyxl flask
```

(Optional) Run this command to start flask if not runnning

```bash
flask run
```

## How to Use

1. **Prepare the Authors Excel File**: Create an Excel file containing the names of authors you wish to search for. List each author's name in a separate row without any headers.

| First name        | Last name |
|-------------------|-----------|
| Firstname;Lastname|           |

2. **Run the Script**: Navigate to the script's directory in your terminal. Execute the script as follows:

   ```bash
    python3 app.py
    ```

   This will start a web server on http://127.0.0.1:5000/. You can open this URL in your browser, upload the Excel file with authors, and retrieve the publications.

    Visit http://127.0.0.1:5000/ in your web browser. Upload your Excel file with the authors, and after processing, you'll be provided with a download link for the extracted publications.

3. **Review the Output**: Check in your `/Downloads` directory or wherever your downloaded files goes for the output Excel file. It contains columns for publication titles, authors involved in that publication, publication years, and match statuses with authors.

## Notes

- The script includes a delay between API requests to avoid exceeding rate limits. This can be adjusted based on the specific requirements of the APIs being queried.
- Ensure that your internet connection is stable during the script's execution to prevent any interruptions during data retrieval.
- If dblp.org API goes down before the script completes the retrieval, you will get a message in your browser stating that the DBLP server went down before the system completes {list of the remaining authors}

## Troubleshooting

If you encounter any issues, such as missing packages or errors during execution, verify that all required Python packages are installed and that the Excel file paths are correctly specified. For further assistance, consult the documentation for the `pandas` , `requests` , `openpyxl` and `flask` libraries or reach out to me for support.