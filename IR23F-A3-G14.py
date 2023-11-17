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

def process_file_for_query(file_path, query_tokens):
    print(f"Processing file: {file_path}")  # Print the file being processed
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
        soup = BeautifulSoup(data['content'], 'lxml')
        text = soup.get_text()
        tokens = tokenizer.tokenize(text.lower())
        stemmed_file_tokens = set(stemmer.stem(token) for token in tokens)
        if query_tokens.issubset(stemmed_file_tokens):
            return data['url']
    return None

def process_query(query):
    print("Processing query...")  # Indicates start of query processing
    query_tokens = set(stemmer.stem(token) for token in tokenizer.tokenize(query.lower()))
    matching_urls = []

    for root, dirs, files in os.walk('DEV'):
        print(f"Entering directory: {root}")  # Print the directory being accessed
        for file in files:
            if file.endswith('.json'):
                file_path = os.path.join(root, file)
                url = process_file_for_query(file_path, query_tokens)
                if url:
                    matching_urls.append(url)
                    if len(matching_urls) >= 5:  # Limit to top 5 results
                        print("Top 5 results found, returning results.")  # Indicates that top 5 results have been found
                        return matching_urls

    if not matching_urls:
        print("No results found.")  # Indicates no results were found
    return matching_urls

def interactive_query_processor():
    while True:
        query = input("Enter your query (or type 'exit' to stop): ")
        if query.lower() == 'exit':
            break
        result = process_query(query)
        if result:
            print(f"Results for query '{query}': {result}")
        else:
            print(f"No results found for query: {query}")

if __name__ == "__main__":
    interactive_query_processor()
