import customtkinter as ctk
from tkinter import filedialog,  messagebox
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
    filter_text = search_filter_entry.get().lower()
    inclusion_filters = []
    exclusion_filters = []

    # Commands for sorting-specific fields
    commands = {
        "$alphname": (lambda x: x[-1].lower(), False),
        "$revalphname": (lambda x: x[-1].lower(), True),
        "$alphfirstdate": (lambda x: x[1].lower(), False),
        "$revalphfirstdate": (lambda x: x[1].lower(), True),
        "$alphseconddate": (lambda x: x[2].lower(), False),
        "$revalphseconddate": (lambda x: x[2].lower(), True),
    }

    # Determine the sorting key and order
    sort_key, sort_reverse = None, False
    for cmd, (key_func, reverse) in commands.items():
        if cmd in filter_text:
            sort_key, sort_reverse = key_func, reverse
            filter_text = filter_text.replace(cmd, "")  # Remove command from filter text
            break  # Assuming only one sorting command per search

    filters = filter_text.split()

    for f in filters:
        if f.startswith('+'):
            inclusion_filters.append(f[1:])
        elif f.startswith('-'):
            exclusion_filters.append(f[1:])

    filtered_data = []

    for row in original_content:
        row_text = ' '.join(map(str, row)).lower()
        if all(f in row_text for f in inclusion_filters) and not any(f in row_text for f in exclusion_filters):
            filtered_data.append(row)

    # Sorting filtered data based on the chosen key and order
    if sort_key:
        filtered_data.sort(key=sort_key, reverse=sort_reverse)

    # Displaying the filtered content
    col_names = ["Status", "First Date", "Second Date", "Name"]
    log_text_widget.delete("0.0", tk.END)
    if filtered_data:
        formatted_content = tabulate(filtered_data, headers=col_names, tablefmt="pipes")
        log_text_widget.insert("0.0", formatted_content)
    else:
        log_text_widget.insert("0.0", "No matches found.")


def save_as_file(log_text_widget):
    # Prompt the user to specify a file name and location
    filepath = filedialog.asksaveasfilename(defaultextension="txt",
                                            filetypes=[("Text Files", "*.txt"), ("All Files", "*.*")])
    if filepath:
        try:
            # Read the content from log_text_widget
            content_to_save = log_text_widget.get("1.0", tk.END)
            # Write the content to the specified file
            with open(filepath, 'w') as file:
                file.write(content_to_save)
            messagebox.showinfo("Success", "File was saved successfully!")
        except Exception as e:
            # If there is any error, show an error message
            messagebox.showerror("Error", f"Failed to save file: {str(e)}")


def filter_query(command, log_text_widget
                 ):
    if not command:  # Check if the command is provided
        log_text_widget.insert(tk.END, "No command provided.")
        return

    parts = command.lower().split(' select ')  # Splitting the command on 'mark'

    # Extracting the column from the command (assumes 'from [column]' syntax)
    from_part = parts[0].split()

    # Explicitly handling the 'ANY' condition
    if from_part[1] == 'any':
        column = None
    else:
        column_map = {
            "status": 0,
            "first date": 1,
            "second date": 2,
            "name": 3
            # 'any' is now explicitly handled above via 'column = None'
        }
        column = column_map.get(from_part[1], None)  # Use 'None' to signify 'ANY'

    mark_and_beyond = ' select '.join(parts[1:]).split(' where ')  # Handling parts after 'mark'

    mark_part = mark_and_beyond[0]  # The criteria to include
    but_part = mark_and_beyond[1:]  # Handling exclusion or sorting conditions

    exclude = []
    sort_ascending = None

    # Processing 'but' conditions (exclusion or sorting)
    if but_part:
        but_conditions = but_part[0].split()
        if but_conditions[0] == 'not':
            exclude = but_conditions[1:]
        elif but_conditions[0] == 'alph':
            sort_ascending = True
        elif but_conditions[0] == 'revalph':
            sort_ascending = False

    filtered_data = []

    # Filtering the data based on 'mark' and 'but' conditions
    for row in original_content:
        include_test = (
            mark_part.lower() in ' '.join(str(v).lower() for v in row) if column is None else mark_part.lower() in str(
                row[column]).lower()
        )
        exclude_test = not any(ex.lower() in ' '.join(str(v).lower() for v in row) for ex in exclude)

        if include_test and exclude_test:
            filtered_data.append(row)

    # Sorting the data if required. Note: Sorting 'ANY' is ambiguous and not performed.
    if sort_ascending is not None and column is not None:
        filtered_data.sort(key=lambda x: str(x[column]).lower(), reverse=not sort_ascending)

    # Displaying the filtered content in the log_text_widget
    col_names = ["     Status    ", "          First Date          ", "              Second Date             ",
                 "         Name        "]
    log_text_widget.delete("0.0", tk.END)  # Clear previous content
    if filtered_data:
        formatted_content = tabulate(filtered_data, headers=col_names, tablefmt="pipes")
        log_text_widget.insert(tk.END, formatted_content)
    else:
        log_text_widget.insert(tk.END, "No matches found.")