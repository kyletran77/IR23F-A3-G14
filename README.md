# IR23F-A3-G14
Steven Truong sctruong 36817733 Stephen Lee stephecl 45957482 Kyle Tran kylet7 38842666

Search Engine Application Usage Guide
-------------------------------------

This guide explains how to run and use the Search Engine application developed for Informatics 141/CS 121.

1. Running the Indexer:

   The indexer creates an inverted index from a set of documents. To run the indexer, execute:

   python indexer_csv.py

   This script reads the documents from a specified directory and generates an 'inverted_index.json' file. Make sure you have the required document files in the 'DEV' directory.

2. Starting the Search Interface:

   To start the search interface, run:

   python search_csv.py

   This will open a GUI where you can interact with the search engine.

3. Performing a Query:

   In the GUI:
   - Enter your search query in the text box at the top.
   - Click the 'Search' button.
   - The search results will be displayed in the window below the search bar.

Ensure that you have Python and the necessary libraries (PyQt5, NLTK) installed on your system to run these scripts.
