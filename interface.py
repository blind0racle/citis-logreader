import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
from tabulate import tabulate
from funcs import *

def setup_interface(window):
    ctk.set_appearance_mode("Light")
    ctk.set_default_color_theme("blue")

    window = ctk.CTk()
    window.title("LogReader by blindoracle")
    window.iconbitmap(r'icon.ico')
    window.geometry("900x610")
    window.resizable(False, False)

    # Configure the window grid to have 5 equal-width columns
    for i in range(5):
        window.grid_columnconfigure(i, weight=1)

    # Adjusted the searchbar to span the first 3 columns
    searchbar = ctk.CTkEntry(window, width=500, placeholder_text="Enter path or browse the file")
    searchbar.grid(row=0, column=0, columnspan=3, padx=20, pady=10, sticky="ew")

    # Adjusted button positions according to new requirements
    browse_btn = ctk.CTkButton(window, text="Browse Files", command=lambda: browse_files(searchbar, log_text_widget))
    browse_btn.grid(row=0, column=3, padx=0, pady=5, sticky="e")

    save_btn = ctk.CTkButton(window, text="Save", command=lambda: save_as_file(log_text_widget))
    save_btn.grid(row=0, column=4, padx=0, pady=5, )

    # log_text_widget to span all 5 columns
    log_text_widget = ctk.CTkTextbox(window, width=860, height=510, font=('Arial', 15))
    log_text_widget.grid(row=1, column=0, columnspan=5, padx=20, pady=0, sticky="ew")

    # Adjusted the third row as per the requirements
    # search_filter_entry now spans the third and fourth columns
    search_filter_entry = ctk.CTkEntry(window, width=150, placeholder_text="'+' to add, '-' to remove")
    search_filter_entry.grid(row=2, column=2, columnspan=2, padx=5, pady=10, sticky='ew')
    search_filter_entry.bind("<Return>", lambda event: filter_content(search_filter_entry, log_text_widget))

    # Moved find_btn to column 4 in the third row
    find_btn = ctk.CTkButton(window, text="Find", command=lambda: filter_content(search_filter_entry, log_text_widget))
    find_btn.grid(row=2, column=4, padx=20, pady=10)

    window.mainloop()
