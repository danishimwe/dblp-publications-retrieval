from flask import Flask, render_template, request, send_file, jsonify
import pandas as pd
import os
import time
import requests
from werkzeug.utils import secure_filename
import unicodedata

app = Flask(__name__)

# Define the directory to save uploaded files and results
UPLOAD_FOLDER = 'uploads'
RESULT_FOLDER = 'files'

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

if not os.path.exists(RESULT_FOLDER):
    os.makedirs(RESULT_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['RESULT_FOLDER'] = RESULT_FOLDER

def normalize_name(name):
    """
    Normalize names by removing special characters and converting them to lowercase.
    """
    name = unicodedata.normalize('NFKD', name).encode('ASCII', 'ignore').decode('ASCII')
    return name.replace(';', ' ').strip().lower()

def retrieve_authors_publications(authors_file, output_file):
    try:
        file_ext = os.path.splitext(authors_file)[1].lower()

        if file_ext == '.csv':
            try:
                given_authors = pd.read_csv(authors_file, header=None, encoding='utf-8').values.flatten().tolist()
            except UnicodeDecodeError:
                given_authors = pd.read_csv(authors_file, header=None, encoding='latin1').values.flatten().tolist()
        elif file_ext in ['.xls', '.xlsx', '.xlsm']:
            given_authors = pd.read_excel(authors_file, header=None).values.flatten().tolist()
        else:
            raise ValueError("Unsupported file format. Please upload a CSV or Excel file.")

        given_authors = [normalize_name(author) for author in given_authors]
        publications_df = pd.DataFrame(columns=['Title', 'Authors', 'Year', 'Match Status'])
        failed_authors = set()  # Use a set to ensure no duplicate authors

        for author in given_authors:
            print(f"Retrieving publications for author: {author}")
            api_url_1 = f'https://dblp.org/search/publ/api?q={author}&format=json&h=1000'
            api_url_2 = f'https://dblp.org/search/publ/api?q={author}&format=json&h=1000&f=1000'

            for api_url in [api_url_1, api_url_2]:
                response = requests.get(api_url)

                if response.status_code != 200:
                    print(f"Error: Received status code {response.status_code} from {api_url}")
                    if response.status_code == 429:
                        failed_authors.add(author)  # Add to failed authors set
                    break  # Skip to the next author if there is an error

                try:
                    data = response.json()
                except ValueError:
                    print(f"Error: Received invalid JSON from {api_url}")
                    failed_authors.add(author)  # Add to failed authors set
                    break  # Skip to the next author

                hits = data.get('result', {}).get('hits', {}).get('hit', [])
                if not isinstance(hits, list):
                    failed_authors.add(author)
                    break  # Skip to the next author

                print(f"Found {len(hits)} publications for author {author}")

                for result in hits:
                    title = result.get('info', {}).get('title', '')
                    authors_info = result.get('info', {}).get('authors', {}).get('author', [])
                    if isinstance(authors_info, list):
                        normalized_authors = [normalize_name(a.get('text', '')) for a in authors_info]
                        matching_authors = [a for a in normalized_authors if a in given_authors]
                    else:
                        normalized_author = normalize_name(authors_info.get('text', ''))
                        matching_authors = [normalized_author] if normalized_author in given_authors else []

                    if matching_authors:
                        authors = ', '.join(matching_authors)
                        match_status = 'Exact Match with given Authors list'
                    else:
                        authors = ', '.join([normalize_name(a.get('text', '')) for a in authors_info]) if isinstance(authors_info, list) else ''
                        match_status = 'No Exact Match Found'

                    year = result.get('info', {}).get('year', '')

                    publications_df = pd.concat([publications_df, pd.DataFrame({'Title': [title], 'Authors': [authors], 'Year': [year], 'Match Status': [match_status]})],
                                                ignore_index=True)

                time.sleep(5)

        print(f"Total publications matched: {len(publications_df)}")

        publications_df = publications_df[publications_df['Match Status'] != 'No Exact Match Found']
        publications_df = publications_df.drop_duplicates(subset=['Title', 'Authors', 'Year'])
        publications_df.to_excel(output_file, index=False)

        return len(publications_df), list(failed_authors)  # Convert set back to list for JSON serialization
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        failed_authors.add(author)  # Add to failed authors set
        raise e

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"error": "No file part"}), 400
    file = request.files['file']
    if file.filename == '':
        return jsonify({"error": "No selected file"}), 400

    try:
        filename = secure_filename(file.filename)
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
        file.save(filepath)

        output_filename = f"{os.path.splitext(filename)[0]}_extracted_publications.xlsx"
        output_file_path = os.path.join(app.config['RESULT_FOLDER'], output_filename)

        publication_count, failed_authors = retrieve_authors_publications(filepath, output_file_path)

        return jsonify({
            "filename": output_filename,
            "publication_count": publication_count,
            "failed_authors": failed_authors  # Ensure failed authors are sent back
        })
    except ValueError as ve:
        print(f"ValueError: {str(ve)}")
        return jsonify({"error": str(ve)}), 400
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": "An error occurred while processing the file."}), 500


@app.route('/download/<filename>')
def download_file(filename):
    return send_file(os.path.join(app.config['RESULT_FOLDER'], filename), as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
