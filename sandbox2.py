import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
from main import reader
from tabulate import tabulate

original_content = []
ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

data=[]
def browse_files():
    filename = filedialog.askopenfilename()
    searchbar.delete(0, ctk.END)
    searchbar.insert(0, filename)


def open_file():
    global original_content  # Ensures we are modifying the global variable
    filepath = searchbar.get()
    linenum=0
    data=[]  # Clear previous data if any from the global list
    try:
        with open(filepath, 'r') as file_content:
            col_names = ["     Status    ", "          First Date          ", "              Second Date             ", "         Name        "]
            for line in file_content:
                linenum += 1
                status, first_date, second_date, name = reader(linenum, filepath)
                data.append([status, first_date, second_date, name])

            log_text_widget.delete("0.0", tk.END)
            formatted_content = tabulate(data, headers=col_names, tablefmt="pipes")
            log_text_widget.insert("0.0", formatted_content)
            original_content = data[:]  # Make a copy of the data for filtering purposes
    except Exception as e:
        log_text_widget.delete("0.0", tk.END)
        log_text_widget.insert("0.0", f"Error opening file: {str(e)}")


def filter_content():
    filter_text = search_filter_entry.get()
    inclusion_filters = []
    exclusion_filters = []

    # Splitting based on space to get all filters
    filters = filter_text.split()

    for f in filters:
        if f.startswith('+'):
            inclusion_filters.append(f[1:].lower())  # Include terms without '+'
        elif f.startswith('-'):
            exclusion_filters.append(f[1:].lower())  # Exclude terms without '-'

    filtered_data = []

    for row in original_content:
        row_text = ' '.join(map(str, row)).lower() # Convert row data to a single lowercase string for comparison
        # Apply inclusion filters if specified, else consider the row
        if all(f in row_text for f in inclusion_filters):
            # Exclude rows that contain any exclusion filter terms
            if not any(f in row_text for f in exclusion_filters):
                filtered_data.append(row)

    # Displaying the filtered content
    col_names = ["     Status    ", "          First Date          ", "              Second Date             ", "         Name        "]
    log_text_widget.delete("0.0", tk.END)
    if filtered_data:
        formatted_content = tabulate(filtered_data, headers=col_names, tablefmt="pipes")
        log_text_widget.insert("0.0", formatted_content)
    else:
        log_text_widget.insert("0.0", "No matches found.")



# Initialize the main window
window = ctk.CTk()
window.title("LogReader by blindoracle")
window.iconbitmap("eye.ico")
window.geometry("900x610")
window.resizable(False, False)

searchbar = ctk.CTkEntry(window, width=500)
searchbar.grid(row=0, column=0, padx=20, pady=10)

browse_btn = ctk.CTkButton(window, text="Browse Files", command=browse_files)
browse_btn.grid(row=0, column=1, padx=0, pady=5)

open_btn = ctk.CTkButton(window, text="Open", command=open_file)
open_btn.grid(row=0, column=2, padx=0, pady=5)

# Replacing the Text widget with CTkTextbox
log_text_widget = ctk.CTkTextbox(window, width=860, height=510)
log_text_widget.grid(row=1, column=0, columnspan=3, padx=20, pady=0)

# Adding search filter entry and button at the bottom
search_filter_entry = ctk.CTkEntry(window, width=150)
search_filter_entry.grid(row=2, column=1, padx=5, pady=10, sticky='ew')

find_btn = ctk.CTkButton(window, text="Find", command=filter_content, width=150)
find_btn.grid(row=2, column=2, padx=20, pady=10, sticky='e')

window.mainloop()