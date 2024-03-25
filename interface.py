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
    window.iconbitmap("eye.ico")
    window.geometry("900x610")
    window.resizable(False, False)

    searchbar = ctk.CTkEntry(window, width=500, placeholder_text="Enter path or browse the file")
    searchbar.grid(row=0, column=0, padx=20, pady=10)

    browse_btn = ctk.CTkButton(window, text="Browse Files", command=lambda: browse_files(searchbar, log_text_widget))
    browse_btn.grid(row=0, column=1, padx=0, pady=5)

    open_btn = ctk.CTkButton(window, text="Save")
    open_btn.grid(row=0, column=2, padx=0, pady=5)

    # Replacing the Text widget with CTkTextbox
    log_text_widget = ctk.CTkTextbox(window, width=860, height=510, font=('Arial', 15))
    log_text_widget.grid(row=1, column=0, columnspan=3, padx=20, pady=0)

    # Adding search filter entry and button at the bottom
    search_filter_entry = ctk.CTkEntry(window, width=150, placeholder_text="'+' to add, '-' to remove")
    search_filter_entry.grid(row=2, column=1, padx=5, pady=10, sticky='ew')
    search_filter_entry.bind("<Return>", lambda event, sfe=search_filter_entry, ltw=log_text_widget: filter_content(sfe, ltw))

    find_btn = ctk.CTkButton(window, text="Find", width=150, command=lambda: filter_content(search_filter_entry, log_text_widget))
    find_btn.grid(row=2, column=2, padx=20, pady=10, sticky='e')

    window.mainloop()