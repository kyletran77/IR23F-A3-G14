import csv
import sys
import json
import time
import math
import ast
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtGui import QFont, QIcon
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer

# Set the field size limit to a higher value
csv.field_size_limit(sys.maxsize)

# nltk for processing text
tokenizer = RegexpTokenizer(r'\w+')
stemmer = PorterStemmer()

# Load id dictionary
id_file = open('id.csv', 'r')
id_reader = csv.reader(id_file)
id_dict = {row[0]: row[1] for row in id_reader}
id_file.close()

def tf_idf_score(query_tokens, document, inverted_index, total_docs, doc_freqs):
    score = 0
    for token in query_tokens:
        tf = 1 if document in inverted_index.get(token, {}) else 0
        df = doc_freqs.get(token, 0)
        idf = math.log((total_docs / (1 + df)) + 1)
        score += (tf * idf)
    return score

def search_with_index(query, index_file='inverted_index.csv'):
    start_time = time.time()
    query_tokens = set(stemmer.stem(token) for token in tokenizer.tokenize(query.lower()))
    inverted_index = {}
    with open(index_file, 'r') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            token = row[0]
            if token in query_tokens:
                link_ids = ast.literal_eval(row[1])
                inverted_index[token] = set(link_ids)
    total_docs = sum(len(token_set) for token_set in inverted_index.values())
    doc_freqs = {token: len(docs) for token, docs in inverted_index.items()}
    document_scores = {}
    for token in query_tokens:
        if token in inverted_index:
            for document in inverted_index[token]:
                document_scores[document] = document_scores.get(document, 0) + \
                                            tf_idf_score(query_tokens, document, inverted_index, total_docs, doc_freqs)
    end_time = time.time()
    response_time_ms = (end_time - start_time) * 1000
    ranked_documents = sorted(document_scores, key=document_scores.get, reverse=True)
    return ranked_documents, response_time_ms

class SearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Best Search Engine for Informatics 141/CS 121')
        self.setWindowIcon(QIcon('search_icon.png'))  # Set your icon file here

        layout = QVBoxLayout()

        self.search_bar = QLineEdit(self)
        self.search_bar.setFont(QFont('Arial', 20))
        self.search_bar.setStyleSheet("padding: 8px;")
        layout.addWidget(self.search_bar)

        search_button = QPushButton('Search', self)
        search_button.setFont(QFont('Arial', 20))
        search_button.setStyleSheet("...")
        search_button.clicked.connect(self.on_search)
        layout.addWidget(search_button)

        self.results_area = QTextEdit(self)
        self.results_area.setFont(QFont('Arial', 20))
        self.results_area.setReadOnly(True)
        layout.addWidget(self.results_area)

        self.setLayout(layout)

    def on_search(self):
        query = self.search_bar.text()
        results, response_time_ms = search_with_index(query)
        num_results = len(results)  # Get the number of results
        result_text = f"Response Time: {response_time_ms:.2f} ms\nNumber of Results: {num_results}\n\n"
        result_text += "\n".join([f'[{result}]{id_dict.get(str(result), "")}' for result in results]) if results else "No results found."
        self.results_area.setText(result_text)


def main():
    app = QApplication(sys.argv)
    ex = SearchApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
