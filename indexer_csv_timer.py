
import json
import csv
import os
from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import warnings
import time
import threading

tokenizer = RegexpTokenizer(r'\w+')
stemmer = PorterStemmer()
inverted_index = defaultdict(list)

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

id_count = 0

# CSV Files Paths and Fieldnames #
# tempfile = NamedTemporaryFile(mode='w', delete=False)
csv_file_path = 'inverted_index.csv'
csv_index = ['token','id']

csv_id = 'id.csv'
id_fields = ['id','url','source']
#*******************************#
simhash_index = defaultdict(list)  # Dictionary to store simhash values

def get_features(text):
    # Function to generate features for Simhash
    tokens = tokenizer.tokenize(text.lower())
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return stemmed_tokens

def is_near_duplicate(simhash_value):
    # Function to check if a document is a near-duplicate
    for existing_simhash in simhash_index.values():
        if simhash_value.distance(existing_simhash) < 5:  # Threshold for similarity
            return True
    return False
#*******************************#

def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        # if not is_near_duplicate(simhash_value):
            # simhash_index[os.path.basename(file_path)] = simhash_value
            # tokens = tokenizer.tokenize(text.lower())
            # stemmed_tokens = [stemmer.stem(token) for token in tokens]
            # return stemmed_tokens, data['url'], os.path.basename(file_path)

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
        csv_file.flush()  # Flush the internal buffer
        csv_file.close()  # Explicitly close the file

    #inverted_index.clear()
def display_timer(start_time):
    while not stop_timer_event.is_set():
        elapsed_time = time.time() - start_time
        print(f"\rElapsed Time: {elapsed_time:.2f} seconds", end="")
        time.sleep(1)  # Update every 1 second


if __name__ == "__main__":
    # start_time = time.time()  # Start the timer

    # file_exists = os.path.isfile(csv_file_path)
    # if not file_exists:
    #     process_directory()
    #     save_inverted_index()

    # end_time = time.time()  # Stop the timer
    # total_time_ms = (end_time - start_time) * 1000  # Convert to milliseconds

    # print(f"Total processing time: {total_time_ms:.2f} ms")
    start_time = time.time()
    stop_timer_event = threading.Event()
    timer_thread = threading.Thread(target=display_timer, args=(start_time,))
    timer_thread.start()

    file_exists = os.path.isfile(csv_file_path)
    if not file_exists:
        process_directory()
        save_inverted_index()

    stop_timer_event.set()
    timer_thread.join()

    end_time = time.time()
    total_time_ms = (end_time - start_time) * 1000
    print(f"\nTotal processing time: {total_time_ms:.2f} ms")