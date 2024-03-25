import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
from tabulate import tabulate
from interface import *

data=[]
original_content = []
def date_beautifier(input_string):

    pairs = [input_string[i:i+2] for i in range(0, len(input_string), 2)]
    numbers = [pair.zfill(2) for pair in pairs]

    num_3 = numbers[3]
    num_4 = numbers[4]
    num_5 = numbers[5]
    num_2 = numbers[2]
    num_1 = numbers[1]
    num_0 = '20' + numbers[0]

    # Format the numbers into the desired string format
    formatted_string = f"{num_3}:{num_4}:{num_5} {num_2}/{num_1}/{num_0}"

    # Print the formatted string
    return formatted_string

def reader(line_number,path):
    with open(path, "r") as file:
        # Read the file line by line
        for index, line in enumerate(file, start=1):
            if index == line_number:
                parts = line.split()

                status = "verified" if parts[0] == "V" else "revoked"
                date1 = date_beautifier(parts[1][:-1])
                if len(parts) == 6:
                    date2 = date_beautifier(parts[2][:-1])
                    cn = parts[5].split("=")[6].split("/")[0]
                else:
                    date2 = "not-stated"
                    cn = parts[4].split("=")[6].split("/")[0]
                return status, date1, date2, cn
        else:
            print("Line number not found in the log file.")

def browse_files(searchbar, log_text_widget):

    filename = filedialog.askopenfilename()
    searchbar.delete(0, ctk.END)
    searchbar.insert(0, filename)
    open_file(searchbar, log_text_widget)


def open_file(searchbar, log_text_widget):
    filepath = searchbar.get()
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


def filter_content(search_filter_entry, log_text_widget):
    filter_text = search_filter_entry.get()
    inclusion_filters = []
    exclusion_filters = []
    filters = filter_text.split()

    for f in filters:
        if f.startswith('+'):
            inclusion_filters.append(f[1:].lower())  # Include terms without '+'
        elif f.startswith('-'):
            exclusion_filters.append(f[1:].lower())  # Exclude terms without '-'

    filtered_data = []

    for row in original_content:
        row_text = ' '.join(map(str, row)).lower() # Convert row data to a single lowercase string for comparison
        if all(f in row_text for f in inclusion_filters):
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
