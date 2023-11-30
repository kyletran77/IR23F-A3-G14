# indexer.py

import json
import os
from bs4 import BeautifulSoup
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import warnings

warnings.filterwarnings("ignore", category=UserWarning, module='bs4')

# Setup tokenizer and stemmer
tokenizer = RegexpTokenizer(r'\w+')
stemmer = PorterStemmer()

# Function to create an inverted index
def create_inverted_index(directory):
    inverted_index = {}
    for root, _, files in os.walk(directory):
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                with open(file_path, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                    soup = BeautifulSoup(data['content'], 'lxml')
                    text = soup.get_text()
                    tokens = tokenizer.tokenize(text.lower())
                    stemmed_tokens = set(stemmer.stem(token) for token in tokens)

                    for token in stemmed_tokens:
                        if token not in inverted_index:
                            inverted_index[token] = {}
                        if file not in inverted_index[token]:
                            inverted_index[token][file] = 0
                        inverted_index[token][file] += 1

    # Save the inverted index to a file
    with open('inverted_index.json', 'w') as f:
        json.dump(inverted_index, f)

if __name__ == "__main__":
    create_inverted_index('DEV')  # Replace 'DEV' with your directory
