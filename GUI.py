import tkinter as tk
from tkinter import filedialog, ttk
import PyPDF2
import pyttsx3
import threading

def browse_pdf():
    file_path = filedialog.askopenfilename(filetypes=[("PDF Files", "*.pdf")])
    pdf_path.set(file_path)


def start_reading():
    pdf_file = pdf_path.get()
    page_number = page_entry.get()

    if not pdf_file:
        status_label.config(text="Please select a PDF file.")
        return

    try:
        page_number = int(page_number)
    except ValueError:
        status_label.config(text="Invalid page number.")
        return

    pdf_reader = PyPDF2.PdfReader(open(pdf_file, 'rb'))

    if page_number < 1 or page_number > len(pdf_reader.pages):
        status_label.config(text="Invalid page number.")
        return

    def read_pdf():
     text = pdf_reader.pages[page_number - 1].extract_text()

     speaker = pyttsx3.init()
     speaker.say(text)
     speaker.runAndWait()

    # Create a new thread for reading the PDF
    pdf_thread = threading.Thread(target=read_pdf)
    pdf_thread.start()

# Create the main window
root = tk.Tk()
root.title("StoryTeller")

# Style
style = ttk.Style()
style.configure('TButton', foreground='white', background='#3498db')
style.configure('TLabel', foreground='#3498db', font=('Helvetica', 12))

# Variables
pdf_path = tk.StringVar()
pdf_path.set("")
page_number = tk.StringVar()
page_number.set("1")

# Labels
ttk.Label(root, text="StoryTeller", font=("Helvetica", 16)).pack(pady=10)
ttk.Label(root, text="Select a PDF file:").pack()
status_label = ttk.Label(root, text="", foreground='red')
status_label.pack()
ttk.Label(root, text="Enter page number:").pack()

# Entry for page number
page_entry = ttk.Entry(root, textvariable=page_number)
page_entry.pack()


# Browse button
browse_button = ttk.Button(root, text="Browse", command=browse_pdf, style="TButton" )
browse_button.pack()

# Start button
start_button = ttk.Button(root, text="Start Reading", command=start_reading)
start_button.pack()

# Run the GUI application
root.mainloop()