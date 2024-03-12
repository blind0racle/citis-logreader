import customtkinter as ctk
from tkinter import filedialog, Text, Scrollbar
import tkinter as tk

ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

window = ctk.CTk()
window.title("LogReader by blindoracle")
window.iconbitmap('eye.ico')
window.geometry("900x600")
window.resizable(False, False)

def browse_files():
    filename = filedialog.askopenfilename()
    searchbar.delete(0, ctk.END)
    searchbar.insert(0, filename)

def open_file():
    filepath = searchbar.get()
    try:
        with open(filepath, 'r') as file_content:
            log_text_widget.delete(1.0, tk.END)
            log_text_widget.insert(tk.END, file_content.read())
    except Exception as e:
        log_text_widget.delete(1.0, tk.END)
        log_text_widget.insert(tk.END, f"Error opening file: {str(e)}")

searchbar = ctk.CTkEntry(window, width=575)
searchbar.grid(row=0, column=0, padx=(10, 5), pady=10)

browse_btn = ctk.CTkButton(window, text="Browse Files", command=browse_files)
browse_btn.grid(row=0, column=1, padx=5, pady=10)

open_btn = ctk.CTkButton(window, text="Open", command=open_file)
open_btn.grid(row=0, column=2, padx=5, pady=10)

# Create the Text widget and corresponding Scrollbar
log_text_widget = Text(window, height=32, width=107, bg="#F2F2F2", fg="#000000", borderwidth=2, relief="solid", padx=10, pady=10)
log_text_widget.grid(row=1, column=0, columnspan=3, padx=10, pady=10)
scrollbar = Scrollbar(window, command=log_text_widget.yview)
scrollbar.grid(row=1, column=3, sticky='nsew')
log_text_widget.config(yscrollcommand=scrollbar.set)

window.mainloop()