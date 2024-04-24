This project is a requirement for CS 006 - Algorithms and Complexity for TIP QC
CS32S1
This is a simple plagiarism checker using multiple python libraries

This Python program provides a basic plagiarism checker for textual content. It allows you to compare two text inputs (source and suspected copy) and calculates similarity scores using different techniques.

Features:

File Support: Opens various file formats including text files, docx, pdf, markdown, rtf, html, csv, json, xml, yaml.
Similarity Scores: Calculates Jaccard Similarity (on word and lemmatized word level) and Cosine Similarity with TF-IDF for a more comprehensive analysis.
Text Preprocessing: Optionally removes stop words (common words like "the", "a") before comparison.
Lemmatization: Converts words to their base form (e.g., "running" to "run") for more accurate comparisons.
Results: Displays Jaccard and Cosine similarity scores along with a plagiarism classification (high, medium, low similarity). It also highlights potential matching phrases between the texts.
How to Use:

Install Required Libraries: Make sure you have the necessary Python libraries installed (nltk, tkinter, PyPDF2, docx, etc.) Use pip install <library_name> to install missing libraries.
Run the Script: Execute the script ALGOPlagiarismChecker.py.
Open Files: Click the "Open File 1" and "Open File 2" buttons to select the source and suspected content files. Supported file formats are listed above.
(Optional) Clear Text: Use the "Clear Text" buttons to clear the content in each text entry box.
Check Plagiarism: Click the "Check Plagiarism" button to analyze the texts and view the results.
Results Interpretation:

High Similarity: A high similarity score (along with highlighted matching phrases) suggests potential plagiarism. Consider revising the content and citing sources appropriately.
Medium Similarity: Moderate similarity might indicate paraphrasing or close rephrasing. Review the highlighted phrases and ensure proper citation if necessary.
Low Similarity: A low similarity score suggests the content is likely original.

Disclaimer:
This is a basic plagiarism checker for educational purposes. It might not capture all plagiarism techniques and for critical tasks, consider using more advanced plagiarism detection tools.

for program demonstration, run:
pip install nltk tkinter PyPDF2 docx markdown striprtf beautifulsoup4 csv json xml.etree sklearn numpy matplotlib


