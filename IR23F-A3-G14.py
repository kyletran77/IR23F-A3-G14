import json
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
        soup = BeautifulSoup(data['content'], 'html.parser')
        text = soup.get_text()
        tokens = tokenizer.tokenize(text.lower())
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        return stemmed_tokens


for root, dirs, files in os.walk('path_to_your_data'):
    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(root, file)
            tokens = process_file(file_path)
            for token in tokens:
                inverted_index[token].append(file_path) # You should include document ID and term frequency


with open('inverted_index.json', 'w') as index_file:
    json.dump(inverted_index, index_file)