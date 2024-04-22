import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
import PyPDF2
import docx
import markdown
import striprtf
from bs4 import BeautifulSoup
import csv
import json
import xml.etree.ElementTree as ET
import yaml

# Define the Jaccard Similarity function
def jaccard_similarity(text1, text2, shingle_size=4):
    shingles1 = set([text1[i:i + shingle_size] for i in range(len(text1) - shingle_size + 1)])
    shingles2 = set([text2[i:i + shingle_size] for i in range(len(text2) - shingle_size + 1)])
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

# Define the function to check plagiarism
def check_plagiarism(text_entry1, text_entry2, result_label):
    text1 = text_entry1.get("1.0", tk.END)[:-1].lower()
    text2 = text_entry2.get("1.0", tk.END)[:-1].lower()

    # Remove punctuation from both texts
    text1 = ''.join(c for c in text1 if c not in set(".,?!:;-'"))
    text2 = ''.join(c for c in text2 if c not in set(".,?!:;-'"))

    similarity = jaccard_similarity(text1, text2)
    intersection_text = ""

    for shingle in set(text1.split()).intersection(set(text2.split())):
        if len(shingle) > 0:
            intersection_text += shingle + " "

    result_text = f"Jaccard Similarity Score: {similarity:.2f}\n"
    result_text += f"Similar words / phrases: {intersection_text}\n"

    if similarity > 0.7:
        result_text = "High similarity detected, potential plagiarism found!\n\n"
        result_text += f"Similar words / phrases: {intersection_text}"
        result_label.config(fg="red", text=result_text)
        messagebox.showerror("Plagiarism Alert", result_text)
    else:
        result_text = "Similarity is low, likely original content.\n\n"
        result_text += f"Similar words / phrases: {intersection_text}"
        result_label.config(fg="green", text=result_text)
        messagebox.showinfo("No Plagiarism", result_text)

    result_label.config(text=result_text)


# Define the main function
def main():
    root = tk.Tk()
    root.title("Plagiarism Checker")

    # Create a frame to hold the widgets
    frame = tk.Frame(root, bg="white", padx=20)
    frame.pack(fill=tk.BOTH, expand=True)

    # Create text entry widgets
    text_entry1 = tk.Text(frame, height=10, width=50, bd=2, relief="solid")
    text_entry1.pack(pady=10)

    open_button1 = tk.Button(frame, text="Open File 1", command=lambda: open_file(text_entry1), bg="lightblue", fg="black")
    open_button1.pack(pady=5, anchor="w")

    clear_button1 = tk.Button(frame, text="Clear Text", command=lambda: clear_text(text_entry1), bg="red", fg="white")
    clear_button1.pack(pady=5, anchor="w")

    text_entry2 = tk.Text(frame, height=10, width=50, bd=2, relief="solid")
    text_entry2.pack(pady=10)

    open_button2 = tk.Button(frame, text="Open File 2", command=lambda: open_file(text_entry2), bg="lightblue", fg="black")
    open_button2.pack(pady=5, anchor="w")

    clear_button2 = tk.Button(frame, text="Clear Text", command=lambda: clear_text(text_entry2), bg="red", fg="white")
    clear_button2.pack(pady=5, anchor="w")

    check_button = tk.Button(frame, text="Check Plagiarism", command=lambda: check_plagiarism(text_entry1, text_entry2, result_label), bg="green", fg="white")
    check_button.pack(pady=10)

    clear_button = tk.Button(frame, text="Clear all Texts", command=lambda: clear_all_text(text_entry1, text_entry2) , bg="red", fg="white")
    clear_button.pack(pady=5, anchor="w")

    # Create a label to display the result
    result_label = tk.Label(frame, text="Jaccard Similarity Score: N/A", font=("Arial", 12), bg="white")
    result_label.pack(pady=10)

    # Start the Tkinter main loop
    root.mainloop()

def clear_text(text_entry):
    text_entry.delete("1.0", tk.END)

def clear_all_text(text_entry1, text_entry2):
    text_entry1.delete("1.0", tk.END) 
    text_entry2.delete("1.0", tk.END)

# Call the main function when the script is executed
if __name__ == "__main__":
    main()
