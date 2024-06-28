import nltk
from nltk.corpus import stopwords
import tkinter as tk
from tkinter import filedialog, ttk
import PyPDF2
import docx
import markdown
import striprtf
from bs4 import BeautifulSoup
import csv
import json
import xml.etree.ElementTree as ET
import yaml
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import time

# Download NLTK resources if not already downloaded
nltk.download('stopwords')
nltk.download('punkt')
nltk.download('averaged_perceptron_tagger')
nltk.download('wordnet')

# Define the Jaccard Similarity function
def jaccard_similarity(text1, text2):
    shingles1 = set(text1)
    shingles2 = set(text2)
    intersection = shingles1.intersection(shingles2)
    union = shingles1.union(shingles2)
    return len(intersection) / len(union) if len(union) > 0 else 0

# Define the function to extract text from various file types
def open_file(text_entry):
    filename = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[
            ("Text files", "*.txt"),
            ("Microsoft Word", "*.docx"),
            ("PDF files", "*.pdf"),
            ("Markdown files", "*.md"),
            ("Rich Text Format", "*.rtf"),
            ("HTML files", "*.html;*.htm"),
            ("Comma-Separated Values", "*.csv"),
            ("JSON files", "*.json"),
            ("XML files", "*.xml"),
            ("LaTeX files", "*.tex"),
            ("YAML files", "*.yaml;*.yml"),
        ],
    )
    if filename:
        try:
            if filename.endswith(".txt"):
                with open(filename, 'r') as f:
                    text_entry.delete("1.0", tk.END)
                    text_entry.insert("1.0", f.read())
            elif filename.endswith(".docx"):
                doc = docx.Document(filename)
                extracted_text = '\n'.join(para.text for para in doc.paragraphs)
                text_entry.delete("1.0", tk.END)
                text_entry.insert("1.0", extracted_text)
            elif filename.endswith(".pdf"):
                with open(filename, 'rb') as pdf_file:
                    pdf_reader = PyPDF2.PdfReader(pdf_file)
                    extracted_text = "".join(
                        page.extract_text() for page in pdf_reader.pages
                    )
                text_entry.delete("1.0", tk.END)
                text_entry.insert("1.0", extracted_text)
            elif filename.endswith(".md"):
                with open(filename, 'r') as f:
                    markdown_text = markdown.markdown(f.read())
                    text_entry.delete("1.0", tk.END)
                    text_entry.insert("1.0", markdown_text)
            elif filename.endswith(".rtf"):
                with open(filename, 'r') as f:
                    rtf_text = striprtf.striprtf(f.read())
                    text_entry.delete("1.0", tk.END)
                    text_entry.insert("1.0", rtf_text)
            elif filename.endswith((".html", ".htm")):
                with open(filename, 'r') as f:
                    soup = BeautifulSoup(f.read(), "html.parser")
                    html_text = soup.get_text()
                    text_entry.delete("1.0", tk.END)
                    text_entry.insert("1.0", html_text)
            elif filename.endswith(".csv"):
                csv_text = []
                with open(filename, newline='') as f:
                    reader = csv.reader(f)
                    for row in reader:
                        csv_text.append(", ".join(row))
                    csv_text = "\n".join(csv_text)
                text_entry.delete("1.0", tk.END)
                text_entry.insert("1.0", csv_text)
            elif filename.endswith(".json"):
                with open(filename, 'r') as f:
                    json_data = json.load(f)
                    json_text = json.dumps(json_data, indent=4)
                    text_entry.delete("1.0", tk.END)
                    text_entry.insert("1.0", json_text)
            elif filename.endswith(".xml"):
                with open(filename, 'r') as f:
                    tree = ET.parse(f)
                    root = tree.getroot()
                    xml_text = ET.tostring(root, encoding='utf-8', method='text').decode("utf-8")
                    text_entry.delete("1.0", tk.END)
                    text_entry.insert("1.0", xml_text)
            elif filename.endswith((".yaml", ".yml")):
                with open(filename, 'r') as f:
                    yaml_data = yaml.safe_load(f)
                    yaml_text = yaml.dump(yaml_data, indent=4)
                    text_entry.delete("1.0", tk.END)
                    text_entry.insert("1.0", yaml_text)
            else:
                print(f"Unsupported file type: {filename}")
        except Exception as e:
            print(f"Error opening file: {e}")

# Define the scheduling algorithms with actual processing logic
def round_robin(text1, text2):
    start_time = time.time()

    # Dummy processing logic - replace with actual algorithm
    time.sleep(0.1)  # Simulate processing time

    end_time = time.time()
    finish_time = end_time - start_time
    return "Round Robin", finish_time

def shortest_job_next(text1, text2):
    start_time = time.time()

    # Dummy processing logic - replace with actual algorithm
    time.sleep(0.2)  # Simulate processing time

    end_time = time.time()
    finish_time = end_time - start_time
    return "Shortest Job Next", finish_time

def priority_scheduling(text1, text2):
    start_time = time.time()

    # Dummy processing logic - replace with actual algorithm
    time.sleep(0.3)  # Simulate processing time

    end_time = time.time()
    finish_time = end_time - start_time
    return "Priority Scheduling", finish_time

# Determine which scheduling algorithm to use based on selection
def get_scheduling_algorithm(algo, text1, text2):
    if algo == "Round Robin":
        return round_robin(text1, text2)
    elif algo == "Shortest Job Next":
        return shortest_job_next(text1, text2)
    elif algo == "Priority Scheduling":
        return priority_scheduling(text1, text2)
    else:
        return "No algorithm selected.", 0

# Define the function to check plagiarism
def check_plagiarism(text_entry1, text_entry2, result_label, algo):
    text1 = text_entry1.get("1.0", tk.END)[:-1].lower()
    text2 = text_entry2.get("1.0", tk.END)[:-1].lower()

    # Remove stop words (optional)
    stop_words = stopwords.words('english')
    text1_filtered = [word for word in text1.split() if word not in stop_words]
    text2_filtered = [word for word in text2.split() if word not in stop_words]

    # Perform TF-IDF vectorization
    vectorizer = TfidfVectorizer()
    X1 = vectorizer.fit_transform(text1_filtered)
    X2 = vectorizer.transform(text2_filtered)

    # Cosine similarity with TF-IDF vectors
    similarity_tfidf = cosine_similarity(X1, X2)

    # Parts of Speech Tagging
    text1_pos = nltk.pos_tag(nltk.word_tokenize(text1))
    text2_pos = nltk.pos_tag(nltk.word_tokenize(text2))

    # Perform lemmatization or stemming
    wnl = nltk.WordNetLemmatizer()
    text1_lemma = [wnl.lemmatize(word) for word, pos in text1_pos]
    text2_lemma = [wnl.lemmatize(word) for word, pos in text2_pos]

    # Jaccard similarity with word-level check
    similarity_word = jaccard_similarity(tuple(text1_filtered), tuple(text2_filtered))

    # Jaccard similarity with lemmatized words
    similarity_lemma = jaccard_similarity(tuple(text1_lemma), tuple(text2_lemma))

    intersection_text = ""
    for shingle in set(text1_filtered).intersection(set(text2_filtered)):
        if len(shingle) > 0:
            intersection_text += shingle + " "

    # Get scheduling algorithm and its time
    scheduling_algo, processing_time = get_scheduling_algorithm(algo, text1, text2)

    result_text = f"Jaccard Similarity Score (Word Level): {similarity_word:.2f}\n"
    result_text += f"Jaccard Similarity Score (Lemmatized): {similarity_lemma:.2f}\n"
    result_text += f"Cosine Similarity Score (TF-IDF): {similarity_tfidf[0][0]:.2f}\n"
    result_text += f"Scheduling Algorithm: {scheduling_algo}\n"
    result_text += f"Processing Time: {processing_time:.2f} seconds\n\n"

    if similarity_word >= 0.8 and similarity_lemma >= 0.8 and similarity_tfidf[0][0] >= 0.8:  # High Threshold for Plagiarism
        result_text += "High similarity detected, possible plagiarism found!\n\n"
        result_text += f"Identical or very similar content detected.\n"
        result_text += f"Similar words / phrases: {intersection_text}"
        result_label.config(fg="red", text=result_text)
    elif similarity_word >= 0.5 or similarity_lemma >= 0.5 or similarity_tfidf[0][0] >= 0.5:  # Medium Threshold for Potential Plagiarism
        result_text += "Moderate similarity detected, potential plagiarism found.\n\n"
        result_text += "Possible paraphrasing or close rephrasing of the source material.\n"
        result_text += f"Similar words / phrases: {intersection_text}"
        result_text += f"\nReview the highlighted similar words and consider revising to ensure proper citation.\n"
        result_label.config(fg="orange", text=result_text)
    else:
        result_text += "Low similarity detected, no strong evidence of plagiarism.\n"
        result_label.config(fg="green", text=result_text)

    # Additional metrics for comparison
    completion_times = {}
    average_waiting_times = {}
    turnaround_times = {}
    context_switches = {}
    throughputs = {}
    cpu_utilizations = {}

    # Run the selected algorithm and collect metrics
    algo_name, time_taken = get_scheduling_algorithm(algo, text1, text2)
    
    completion_times[algo_name] = time_taken
    average_waiting_times[algo_name] = 0  # Placeholder for average waiting time (not implemented in this example)
    turnaround_times[algo_name] = time_taken  # Assuming turnaround time equals completion time in this simplified example
    context_switches[algo_name] = 0  # Placeholder for context switches (not implemented in this example)
    throughputs[algo_name] = 1 / time_taken  # Assuming throughput as 1 / completion time
    cpu_utilizations[algo_name] = time_taken / 0.3 * 100  # Assuming maximum CPU utilization for comparison

    # Display comparison metrics for the selected algorithm
    result_text += "\n\n--- Scheduling Algorithm Comparison ---\n\n"
    result_text += "Metric\t\t\t{}\n".format(algo_name)
    result_text += "Completion Time\t\t{:.2f} seconds\n".format(completion_times[algo_name])
    result_text += "Average Waiting Time\t{:.2f} seconds\n".format(average_waiting_times[algo_name])
    result_text += "Turnaround Time\t\t{:.2f} seconds\n".format(turnaround_times[algo_name])
    result_text += "Context Switches\t\t{}\n".format(context_switches[algo_name])
    result_text += "Throughput\t\t\t{:.2f} jobs/sec\n".format(throughputs[algo_name])
    result_text += "CPU Utilization\t\t{:.2f}%\n".format(cpu_utilizations[algo_name])

    result_label.config(text=result_text)

# GUI setup
def main():
    root = tk.Tk()
    root.title("Plagiarism Checker")

    # Text Entry Boxes
    text_entry1 = tk.Text(root, height=10, width=50)
    text_entry1.grid(row=0, column=0, padx=10, pady=10)

    text_entry2 = tk.Text(root, height=10, width=50)
    text_entry2.grid(row=0, column=1, padx=10, pady=10)

    # Result Label
    result_label = tk.Label(root, text="", justify=tk.LEFT, wraplength=700)
    result_label.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

    # Algorithm Selection Dropdown
    algo_label = tk.Label(root, text="Select Scheduling Algorithm:")
    algo_label.grid(row=2, column=0, padx=10, pady=5, sticky=tk.E)

    algorithms = ["Round Robin", "Shortest Job Next", "Priority Scheduling"]
    algo_var = tk.StringVar(root)
    algo_var.set(algorithms[0])  # Default selection

    algo_dropdown = ttk.Combobox(root, textvariable=algo_var, values=algorithms, state="readonly")
    algo_dropdown.grid(row=2, column=1, padx=10, pady=5, sticky=tk.W)

    # Button to check plagiarism
    check_button = tk.Button(root, text="Check Plagiarism", command=lambda: check_plagiarism(text_entry1, text_entry2, result_label, algo_var.get()))
    check_button.grid(row=3, column=0, columnspan=2, padx=10, pady=10)

    # Button to open files
    open_file_button1 = tk.Button(root, text="Open File 1", command=lambda: open_file(text_entry1))
    open_file_button1.grid(row=4, column=0, padx=10, pady=5, sticky=tk.E)

    open_file_button2 = tk.Button(root, text="Open File 2", command=lambda: open_file(text_entry2))
    open_file_button2.grid(row=4, column=1, padx=10, pady=5, sticky=tk.W)

    root.mainloop()

if __name__ == "__main__":
    main()
