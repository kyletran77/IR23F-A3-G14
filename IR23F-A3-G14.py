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
        soup = BeautifulSoup(data['content'], 'html.parser')
        text = soup.get_text()
        tokens = tokenizer.tokenize(text.lower())
        stemmed_tokens = [stemmer.stem(token) for token in tokens]
        return stemmed_tokens, data['url']


for root, dirs, files in os.walk('ANALYST'):
    for file in files:
        if file.endswith('.json'):
            file_path = os.path.join(root, file)
            tokens, tokenurl = process_file(file_path)
            for token in tokens:
                # You should include document ID and term frequency
                if tokenurl not in inverted_index[token]:
                    inverted_index[token].append(tokenurl)

with open('inverted_index.json', 'w') as index_file:
    # sorteddata = {k: v for k, v in sorted(
    #    inverted_index.items(), key=lambda inverted_index: inverted_index[1], reverse=True)}
    json.dump(inverted_index, index_file)
