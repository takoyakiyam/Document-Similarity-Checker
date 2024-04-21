import tkinter as tk
from tkinter import filedialog
import PyPDF2
import docx

# Define the Jaccard Similarity function
def jaccard_similarity(text1, text2, shingle_size=3):
    shingles1 = set([text1[i:i + shingle_size] for i in range(len(text1) - shingle_size + 1)])
    shingles2 = set([text2[i:i + shingle_size] for i in range(len(text2) - shingle_size + 1)])
    intersection = shingles1.intersection(shingles2)
    union = shingles1.union(shingles2)
    return len(intersection) / len(union) if len(union) > 0 else 0

# Define the function to open and read a file
def open_file(text_entry):
    filename = filedialog.askopenfilename(
        title="Select a File",
        filetypes=[("Text files", "*.txt"), ("docx files", "*.docx"), ("PDF files", "*.pdf")]
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
                    extracted_text = "".join(page.extract_text() for page in pdf_reader.pages)
                text_entry.delete("1.0", tk.END)
                text_entry.insert("1.0", extracted_text)
            else:
                print(f"Unsupported file type: {filename}")
        except Exception as e:
            print(f"Error opening file: {e}")

# Define the function to check plagiarism
def check_plagiarism(text_entry1, text_entry2, result_label):
    text1 = text_entry1.get("1.0", tk.END)[:-1]  # Remove trailing newline
    text2 = text_entry2.get("1.0", tk.END)[:-1]
    similarity = jaccard_similarity(text1.lower(), text2.lower())
    result_label.config(text=f"Jaccard Similarity Score: {similarity:.2f}")
    if similarity > 0.7:
        result_label.config(text=result_label.cget("text") + "\nHigh similarity detected, potential plagiarism found!")
    else:
        result_label.config(text=result_label.cget("text") + "\nSimilarity is low, likely original content.")

# Define the main function
def main():
    root = tk.Tk()
    root.title("Plagiarism Checker")

    # Create text entry widgets
    text_entry1 = tk.Text(root, height=10, width=50)
    text_entry2 = tk.Text(root, height=10, width=50)

    # Create buttons for opening files and checking plagiarism
    open_button1 = tk.Button(root, text="Open File 1", command=lambda: open_file(text_entry1))
    open_button2 = tk.Button(root, text="Open File 2", command=lambda: open_file(text_entry2))
    check_button = tk.Button(root, text="Check Plagiarism", command=lambda: check_plagiarism(text_entry1, text_entry2, result_label))

    # Create a label to display the result
    result_label = tk.Label(root, text="Jaccard Similarity Score: N/A")

    # Organize the layout with grid or pack
    text_entry1.pack(pady=10)
    open_button1.pack(pady=5)
    text_entry2.pack(pady=10)
    open_button2.pack(pady=5)
    check_button.pack(pady=10)
    result_label.pack(pady=10)

    # Start the Tkinter main loop
    root.mainloop()

# Call the main function when the script is executed
if __name__ == "__main__":
    main()
