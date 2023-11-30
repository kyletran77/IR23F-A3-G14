
import json
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLineEdit, QPushButton, QTextEdit
from PyQt5.QtGui import QFont, QIcon
from PyQt5.QtCore import Qt
from nltk.stem import PorterStemmer
from nltk.tokenize import RegexpTokenizer
import math


# Setup tokenizer and stemmer
tokenizer = RegexpTokenizer(r'\w+')
stemmer = PorterStemmer()

# Function to search using the inverted index
def tf_idf_score(query_tokens, document, inverted_index, total_docs, doc_freqs):
    score = 0
    for token in query_tokens:
        tf = inverted_index[token][document] if token in inverted_index and document in inverted_index[token] else 0
        df = doc_freqs.get(token, 0)
        idf = math.log(total_docs / (1 + df))  # Adding 1 to avoid division by zero
        score += tf * idf
    return score

def search_with_index(query, index_file='inverted_index.json'):
    with open(index_file, 'r') as f:
        inverted_index = json.load(f)

    total_docs = len({doc for docs in inverted_index.values() for doc in docs})
    doc_freqs = {token: len(docs) for token, docs in inverted_index.items()}
    
    query_tokens = set(stemmer.stem(token) for token in tokenizer.tokenize(query.lower()))
    document_scores = {}

    for token in query_tokens:
        if token in inverted_index:
            for document in inverted_index[token]:
                if document not in document_scores:
                    document_scores[document] = 0
                document_scores[document] += tf_idf_score(query_tokens, document, inverted_index, total_docs, doc_freqs)

    ranked_documents = sorted(document_scores, key=document_scores.get, reverse=True)
    return ranked_documents[:5]  # Return the top 5 results

class SearchApp(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setGeometry(300, 300, 600, 400)
        self.setWindowTitle('Best Search Engine for Informatics 141/CS 121')
        self.setWindowIcon(QIcon('search_icon.png'))  # Add a search icon here

        # Styling
        self.setStyleSheet("background-color: #2c3e50; color: #ecf0f1;")

        layout = QVBoxLayout()

        self.search_bar = QLineEdit(self)
        self.search_bar.setFont(QFont('Arial', 20))
        self.search_bar.setStyleSheet("padding: 8px;")
        layout.addWidget(self.search_bar)

        search_button = QPushButton('Search', self)
        search_button.setFont(QFont('Arial', 20))
        search_button.setStyleSheet("QPushButton { background-color: #3498db; border: none; padding: 8px; color: white; }"
                                    "QPushButton:hover { background-color: #2980b9; }")
        search_button.clicked.connect(self.on_search)
        layout.addWidget(search_button)

        self.results_area = QTextEdit(self)
        self.results_area.setFont(QFont('Arial', 20))
        self.results_area.setReadOnly(True)
        layout.addWidget(self.results_area)

        self.setLayout(layout)

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
