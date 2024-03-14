import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
from main import reader
from tabulate import tabulate


ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

data=[]
def browse_files():
    filename = filedialog.askopenfilename()
    searchbar.delete(0, ctk.END)
    searchbar.insert(0, filename)


def open_file():
    filepath = searchbar.get()
    linenum=0
    try:
        with open(filepath, 'r') as file_content:
            # Preparing headers
            col_names = ["     Status    ", "          First Date          ", "              Second Date             ", "         Name        ", "      Email      "]
            for line in file_content:
                    linenum+=1
                    status, first_date, second_date, name, email = reader(linenum,filepath)
                    data.append([status, first_date, second_date, name, email])

                            # Displaying the formatted content
            log_text_widget.delete("0.0", tk.END)
            log_text_widget.insert("0.0", (tabulate(data, headers=col_names, tablefmt="pipes")))

    except Exception as e:
        log_text_widget.delete("0.0", tk.END)
        log_text_widget.insert("0.0", f"Error opening file: {str(e)}")


def filter_content():
    search_term = search_filter_entry.get()
    all_content = log_text_widget.get("1.0", tk.END)
    filtered_content = ""

    for line in all_content.split("\n"):
        if search_term.lower() in line.lower():
            filtered_content += line + "\n"

    # Displaying the filtered content
    log_text_widget.delete("1.0", tk.END)
    log_text_widget.insert("1.0", filtered_content)



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