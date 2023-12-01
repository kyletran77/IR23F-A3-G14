import json
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import math

# nltk for processing text
tokenizer = RegexpTokenizer(r'\w+')
stemmer = PorterStemmer()

# TF-IDF score calculator
# Basically multiplies term freq by inverse doc freq
def tf_idf_score(query_tokens, document, inverted_index, total_docs, doc_freqs):
    score = 0
    # Loop thru each word in query
    for token in query_tokens:
        tf = inverted_index.get(token, {}).get(document, 0)
        df = doc_freqs.get(token, 0)
        idf = math.log((total_docs / (1 + df)) + 1)  # Math stuff for idf
        score += (tf * idf)  # Add up scores
    return score

# Main search func
def search_with_index(query, index_file='inverted_index.json'):
    # Open inverted index file
    with open(index_file, 'r') as f:
        inverted_index = json.load(f)

    # Counting docs and getting freqs for tf-idf
    total_docs = len({doc for docs in inverted_index.values() for doc in docs})
    doc_freqs = {token: len(docs) for token, docs in inverted_index.items()}
    
    # Processing the user's query
    query_tokens = set(stemmer.stem(token) for token in tokenizer.tokenize(query.lower()))
    document_scores = {}

    # Scoring each doc
    for token in query_tokens:
        if token in inverted_index:
            for document in inverted_index[token]:
                if document not in document_scores:
                    document_scores[document] = 0
                score = tf_idf_score(query_tokens, document, inverted_index, total_docs, doc_freqs)
                document_scores[document] += score

    # Sorting docs based on their score
    ranked_documents = sorted(document_scores, key=document_scores.get, reverse=True)
    return ranked_documents[:5]  # Give back top 5

class SearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    # Setup the GUI layout
    def initUI(self):
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Best Search Engine for Informatics 141/CS 121')
        self.setWindowIcon(QIcon('search_icon.png'))  # Icon for the app

        layout = QVBoxLayout()

        # Text box for search
        self.search_bar = QLineEdit(self)
        self.search_bar.setFont(QFont('Arial', 20))
        self.search_bar.setStyleSheet("padding: 8px;")
        layout.addWidget(self.search_bar)

        # Button for triggering search
        search_button = QPushButton('Search', self)
        search_button.setFont(QFont('Arial', 20))
        search_button.setStyleSheet("...")
        search_button.clicked.connect(self.on_search)
        layout.addWidget(search_button)

        # Area to show search results
        self.results_area = QTextEdit(self)
        self.results_area.setFont(QFont('Arial', 20))
        self.results_area.setReadOnly(True)
        layout.addWidget(self.results_area)

        self.setLayout(layout)

    # What happens when search is clicked
    def on_search(self):
        query = self.search_bar.text()
        results = search_with_index(query)
        result_text = "\n".join(results) if results else "No results found."
        self.results_area.setText(result_text)

def main():
    app = QApplication(sys.argv)
    ex = SearchApp()
    ex.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
