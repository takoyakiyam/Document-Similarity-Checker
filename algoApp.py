import tkinter as tk
from tkinter import filedialog

def jaccard_similarity(text1, text2, shingle_size=3):
  """
  Calculates the Jaccard Similarity between two texts using shingling.

  Args:
      text1: First text string.
      text2: Second text string.
      shingle_size: Size of the shingle (n-gram) to consider.

  Returns:
      Jaccard Similarity score (float) between 0 and 1.
  """
  shingles1 = set([text1[i:i+shingle_size] for i in range(len(text1)-shingle_size+1)])
  shingles2 = set([text2[i:i+shingle_size] for i in range(len(text2)-shingle_size+1)])
  intersection = shingles1.intersection(shingles2)
  union = shingles1.union(shingles2)
  return len(intersection) / len(union) if len(union) > 0 else 0

def open_file(text_entry):
  """
  Opens a file dialog and reads the content into the specified Text widget.
  """
  filename = filedialog.askopenfilename(title="Select a Text File")
  if filename:
    with open(filename, 'r') as f:
      text_entry.delete("1.0", tk.END)  # Clear existing text
      text_entry.insert("1.0", f.read())

def check_plagiarism():
  """
  Retrieves text from input fields, calculates similarity, and displays results.
  """
  global text_entry1, text_entry2, result_label
  text1 = text_entry1.get("1.0", tk.END)[:-1]  # Remove trailing newline
  text2 = text_entry2.get("1.0", tk.END)[:-1]
  similarity = jaccard_similarity(text1.lower(), text2.lower())
  result_label.config(text=f"Jaccard Similarity Score: {similarity:.2f}")
  if similarity > 0.7:  # Adjust threshold as needed
    result_label.config(text=result_label.cget("text") + "\nHigh similarity detected, potential plagiarism found!")
  else:
    result_label.config(text=result_label.cget("text") + "\nSimilarity is low, likely original content.")

def main():
  """
  Creates the Tkinter UI for the plagiarism checker.
  """
  global text_entry1, text_entry2, result_label
  window = tk.Tk()
  window.title("Plagiarism Checker")

  # Text Input Fields (Now defined within main)
  label1 = tk.Label(window, text="Text 1:")
  label1.grid(row=0, column=0)
  text_entry1 = tk.Text(window, width=50, height=10)
  text_entry1.grid(row=0, column=1, columnspan=2)
  button1 = tk.Button(window, text="Import a Text File", command=lambda: open_file(text_entry1))
  button1.grid(row=1, column=0)

  label2 = tk.Label(window, text="Text 2:")
  label2.grid(row=2, column=0)
  text_entry2 = tk.Text(window, width=50, height=10)
  text_entry2.grid(row=2, column=1, columnspan=2)
  button2 = tk.Button(window, text="Import a Text File", command=lambda: open_file(text_entry2))
  button2.grid(row=3, column=0)

  # Check Button
  check_button = tk.Button(window, text="Check Plagiarism", command=check_plagiarism)
  check_button.grid(row=4, column=1, pady=10)

  # Result Label (Now defined within main)
  result_label = tk.Label(window, text="")
  result_label.grid(row=5, columnspan=3)

  window.mainloop()

if __name__ == "__main__":
  main()
