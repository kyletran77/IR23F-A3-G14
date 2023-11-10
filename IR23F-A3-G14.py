import json
import csv
import os
from bs4 import BeautifulSoup
from collections import defaultdict
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer

tokenizer = RegexpTokenizer(r'\w+')
stemmer = PorterStemmer()
inverted_index = defaultdict(list)


def process_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        soup = BeautifulSoup(data['content'], 'lxml')
        text = soup.get_text()
        tokens = tokenizer.tokenize(text.lower())
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        return stemmed_tokens, data['url'], os.path.basename(file_path)


csv_file_path = 'inverted_index.csv'

for root, dirs, files in os.walk('DEV'):
    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(root, file)
            tokens, url, base_name = process_file(file_path)

            for token in set(tokens):
                inverted_index[token].append(base_name)

# Write the inverted index to a CSV file
with open(csv_file_path, 'w', newline='') as csv_file:
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(['Token', 'Files'])

    for token, files in inverted_index.items():
        csv_writer.writerow([token] + files)
