import json
import csv
import os
from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import warnings

tokenizer = RegexpTokenizer(r'\w+')
stemmer = PorterStemmer()
inverted_index = defaultdict(list)

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

id_count = 0

# CSV Files Paths and Fieldnames #
tempfile = NamedTemporaryFile(mode='w', delete=False)
csv_file_path = 'inverted_index.csv'
csv_index = ['token','id']

csv_id = 'id.csv'
id_fields = ['id','url','source']
#*******************************#

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        soup = BeautifulSoup(data['content'], 'lxml')  # Use 'lxml' here
        text = soup.get_text()
        tokens = tokenizer.tokenize(text.lower())
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        return stemmed_tokens, data['url'], os.path.basename(file_path)

def process_directory():
    global inverted_index
    global id_count
    with open(csv_id, 'w') as idDict: 
        writer = csv.DictWriter(idDict, fieldnames=id_fields)
        for root, dirs, files in os.walk('DEV'):
            for file in files:
                if file.endswith('.json'):
                    file_path = os.path.join(root, file)
                    tokens, url, base_name = process_file(file_path)
                    id_count += 1
                    writer.writerow({'id': id_count, 'url': url, 'source': base_name}) # Create a id relation to url and source.

                    for token in set(tokens):
                        inverted_index[token].append(id_count)

        inverted_index = dict(sorted(inverted_index.items()))
    return

# Write the inverted index to a CSV file

def save_inverted_index():
    global inverted_index
    #file_exists = os.path.isfile(csv_file_path)
    # Read existing rows from the file
    # rows = []
    # if file_exists:
    #     with open(csv_file_path, 'r', newline='', encoding='utf-8') as read_file:
    #         rows = list(csv.DictReader(read_file, fieldnames=csv_index))
            

    # for token, id_list in inverted_index.items():
    #     token_exists = any(row['token'] == token for row in rows)
    #     if token_exists:
    #         # Update the existing entry by appending new IDs
    #         for row in rows:
    #             if row['token'] == token:
    #                 row['id'] += ',' + ', '.join(map(str, id_list))
    #                 break
    #     else:
    #         # Add a new entry for the token
    #         rows.append({'token': token, 'id': ', '.join(map(str, id_list))})

        # Write the updated content back to the file
    with open(csv_file_path, 'w', newline='', encoding='utf-8') as csv_file:
        csv_writer = csv.DictWriter(csv_file, fieldnames=csv_index)
        for key, id in inverted_index.items():
            csv_writer.writerow({'token': key, 'id': id})

    #inverted_index.clear()

if __name__ == "__main__":
    file_exists = os.path.isfile(csv_file_path)
    if not file_exists:
        process_directory()
        save_inverted_index()
