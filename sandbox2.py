import customtkinter as ctk
from tkinter import filedialog
import tkinter as tk
from main import reader


ctk.set_appearance_mode("Light")
ctk.set_default_color_theme("blue")

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
            formatted_content = "{:<10}{:<20}{:<20}{:<30}{:<50}\n".format("Status", "First Date", "Second Date", "Name", "Email")
            for line in file_content:
                    linenum+=1
                    status, first_date, second_date, name, email = reader(linenum,filepath)

                    formatted_line = "{:<10}{:<20}{:<20}{:<30}{:<50}".format(
                        status,
                        first_date,
                        second_date,
                        name,
                        email
                    )
                    formatted_content += formatted_line + "\n"

            # Displaying the formatted content
            log_text_widget.delete("0.0", tk.END)
            log_text_widget.insert("0.0", formatted_content)

    except Exception as e:
        log_text_widget.delete("0.0", tk.END)
        log_text_widget.insert("0.0", f"Error opening file: {str(e)}")

# Initialize the main window
window = ctk.CTk()
window.title("LogReader by blindoracle")

window.geometry("900x630")
window.resizable(False, False)

searchbar = ctk.CTkEntry(window, width=520)
searchbar.grid(row=0, column=0, padx=10, pady=20)

browse_btn = ctk.CTkButton(window, text="Browse Files", command=browse_files)
browse_btn.grid(row=0, column=1, padx=5, pady=10)

open_btn = ctk.CTkButton(window, text="Open", command=open_file)
open_btn.grid(row=0, column=2, padx=5, pady=10)

# Replacing the Text widget with CTkTextbox
log_text_widget = ctk.CTkTextbox(window, width=860, height=510)
log_text_widget.grid(row=1, column=0, columnspan=3, padx=20, pady=0)

window.mainloop()